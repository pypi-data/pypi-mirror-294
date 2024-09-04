from datetime import (
    timedelta,
)
from typing import (
    TYPE_CHECKING,
    Any,
)

from django.urls import (
    reverse,
)
from django.utils import (
    timezone,
)
from rest_framework import (
    status,
)
from rest_framework.test import (
    APITransactionTestCase,
)

from edulib.core import (
    bus,
)
from edulib.core.employees.tests.utils import (
    get_employee,
)
from edulib.core.issuance_delivery.tests.utils import (
    get_issuance_delivery,
)
from edulib.core.lib_authors.tests.utils import (
    get_author,
)
from edulib.core.lib_registry.tests.utils import (
    get_registry_entry,
    get_registry_example,
)
from edulib.core.persons.tests.utils import (
    get_person,
)
from edulib.core.readers.tests.utils import (
    get_reader,
)
from edulib.core.schools.tests.utils import (
    get_school,
)


if TYPE_CHECKING:
    from edulib.core.issuance_delivery.domain import (
        IssuanceDelivery,
    )


class IssuanceDeliveryRestTestCase(APITransactionTestCase):
    def setUp(self) -> None:
        self.uow = bus.get_uow()

        self.author = get_author(self.uow)
        self.person = get_person(self.uow)
        self.school = get_school(self.uow)
        self.employee = get_employee(self.uow, person_id=self.person.id, school_id=self.school.id)
        self.reader = get_reader(self.uow, teacher_id=self.employee.id, school_id=self.school.id)
        self.entry = get_registry_entry(self.uow, author_id=self.author.id, school_id=self.school.id)
        self.example = get_registry_example(
            self.uow,
            lib_reg_entry_id=self.entry.id,
            school_id=self.school.id,
            card_number='12345',
        )

        self.initial_data = {
            'example_id': self.example.id,
            'reader_id': self.reader.id,
            'issuance_date': str(timezone.now().date() - timedelta(days=30)),
        }

        self.list_url = reverse('issuances-list')

    def test_issue_example(self) -> None:
        response = self.client.post(
            reverse('issuances-list'),
            self.initial_data | {'examples': [self.example.id]},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data[0])
        json = response.json()[0]
        json.pop('id')
        self.assertDictEqual(
            json,
            self.initial_data
            | {
                'extension_days_count': None,
                'fact_delivery_date': None,
                'special_notes': None,
            },
        )

    def test_deliver_example(self) -> None:
        issuance_delivery = get_issuance_delivery(self.uow, **self.initial_data, school_id=self.school.id)
        delivery_data = {
            'fact_delivery_date': str(timezone.now().date()),
            'special_notes': 'Замечаний нет',
        }

        response = self.client.post(
            reverse('issuances-return'),
            delivery_data | {'issued_ids': [issuance_delivery.id]},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json()[0],
            self.initial_data
            | delivery_data
            | {'id': issuance_delivery.id, 'extension_days_count': issuance_delivery.extension_days_count},
        )

    def test_prolong_issuance(self) -> None:
        issuance_delivery = get_issuance_delivery(self.uow, **self.initial_data, school_id=self.school.id)
        prolong_data = {
            'extension_days_count': 10,
        }

        response = self.client.patch(
            reverse('issuances-detail', kwargs={'pk': issuance_delivery.id}),
            prolong_data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            self.initial_data
            | {
                'id': issuance_delivery.id,
                'extension_days_count': 10,
                'fact_delivery_date': None,
                'special_notes': None,
            },
        )

    def test_auto_issue_examples(self) -> None:
        response = self.client.post(
            reverse('issuances-auto'),
            {
                'issuance_date': self.initial_data['issuance_date'],
                'count': 1,
                'issued': [
                    {
                        'reader_id': self.initial_data['reader_id'],
                        'book_registry_ids': [self.example.lib_reg_entry_id],
                    },
                ],
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data[0])
        json = response.json()[0]
        json.pop('id')
        self.assertDictEqual(
            json,
            self.initial_data
            | {
                'extension_days_count': None,
                'fact_delivery_date': None,
                'special_notes': None,
            },
        )

    def test_list(self) -> None:
        issuance_delivery = get_issuance_delivery(self.uow, **self.initial_data, school_id=self.school.id)

        response = self.client.get(reverse('issuances-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ('count', 'next', 'previous', 'results'):
            with self.subTest(field=field):
                self.assertIn(field, response.data)
        self.assert_issuance_delivery(response.json()['results'][0], issuance_delivery)

    def test_retrieve(self) -> None:
        issuance_delivery = get_issuance_delivery(self.uow, **self.initial_data, school_id=self.school.id)

        response = self.client.get(reverse('issuances-detail', kwargs={'pk': issuance_delivery.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_issuance_delivery(response.json(), issuance_delivery)

    def test_search_by_fields(self) -> None:
        issuance_delivery = get_issuance_delivery(self.uow, **self.initial_data, school_id=self.school.id)
        response = self.client.get(reverse('issuances-detail', kwargs={'pk': issuance_delivery.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        plan_del_date = response.json().get('plan_del_date')
        search_fields = {
            'example__lib_reg_entry__title': self.entry.title,
            'example__card_number': self.example.card_number,
            'issuance_date': issuance_delivery.issuance_date,
            'plan_del_date': plan_del_date,
        }

        for field, value in search_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {'search': value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertGreater(len(results), 0)
                self.assert_issuance_delivery(results[0], issuance_delivery)

    def test_search_by_nonexistent_values(self) -> None:
        get_issuance_delivery(self.uow, **self.initial_data, school_id=self.school.id)
        search_fields = {
            'example__lib_reg_entry__title': 'NonExistentTitle',
            'example__card_number': '00000',
            'issuance_date': '3025-09-09',
            'plan_del_date': '3025-09-09'
        }

        for field, value in search_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {'search': value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertEqual(len(results), 0)

    def test_filter_by_fields(self) -> None:
        issuance_delivery = get_issuance_delivery(self.uow, **self.initial_data, school_id=self.school.id)
        response = self.client.get(reverse('issuances-detail', kwargs={'pk': issuance_delivery.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        plan_del_date = response.json().get('plan_del_date')
        filter_fields = {
            'author_name': self.author.name,
            'example_title': self.entry.title,
            'plan_del_date': plan_del_date,
            'example_id': self.example.id,
            'reader_id': self.reader.id,
        }

        for field, value in filter_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, data={field: value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertGreater(len(results), 0)
                self.assert_issuance_delivery(results[0], issuance_delivery)

    def test_filter_by_nonexistent_values(self) -> None:
        get_issuance_delivery(self.uow, **self.initial_data, school_id=self.school.id)

        filter_fields = {
            'author_name': 'Вымышленный А.Б.',
            'example_title': 'Вымышленный учебник',
            'plan_del_date': '3025-09-09',
            'example_id': 9999,
            'reader_id': 9999,
        }

        for field, value in filter_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {field: value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertEqual(len(results), 0)

    def assert_issuance_delivery(
        self,
        response: dict[str, Any],
        issuance_delivery: 'IssuanceDelivery',
    ) -> None:
        self.assertDictEqual(
            response,
            {
                'id': issuance_delivery.id,
                'issuance_date': str(issuance_delivery.issuance_date),
                'fact_delivery_date': None,
                'special_notes': None,
                'extension_days_count': issuance_delivery.extension_days_count,
                'reader': {
                    'id': self.reader.id,
                    'number': self.reader.number,
                    'firstname': self.person.firstname,
                    'surname': self.person.surname,
                    'patronymic': self.person.patronymic,
                },
                'example': {
                    'id': self.example.id,
                    'title': self.entry.title,
                    'author': {
                        'id': self.author.id,
                        'name': self.author.name,
                    },
                    'card_number': self.example.card_number,
                    'max_date': self.example.max_date,
                },
                'plan_del_date': str(
                    issuance_delivery.issuance_date
                    + timedelta(days=issuance_delivery.extension_days_count + int(self.example.max_date))
                ),
            },
        )
