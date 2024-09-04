from typing import (
    Any,
)

from django.urls import (
    reverse,
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
from edulib.core.academic_years.tests.utils import (
    get_academic_year,
)
from edulib.core.classyears.tests.utils import (
    get_class_year,
)
from edulib.core.employees.tests.utils import (
    get_employee,
)
from edulib.core.issuance_delivery.tests.utils import (
    get_issuance_delivery,
)
from edulib.core.lib_registry.tests.utils import (
    get_registry_example,
)
from edulib.core.parallels.tests.utils import (
    get_parallel,
)
from edulib.core.persons.tests.utils import (
    get_person,
)
from edulib.core.readers.domain import (
    ReaderRole,
)
from edulib.core.readers.tests.utils import (
    get_reader,
)
from edulib.core.schools.tests.utils import (
    get_school,
)


class ReaderRestTests(APITransactionTestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        self.uow = bus.get_uow()

        self.person = get_person(self.uow)
        self.school = get_school(self.uow)
        self.academic_year = get_academic_year(self.uow)
        self.parallel = get_parallel(self.uow)
        self.employee = get_employee(self.uow, person_id=self.person.id, school_id=self.school.id)
        self.class_year = get_class_year(
            self.uow,
            school_id=self.school.id,
            teacher_id=self.employee.id,
            parallel_id=self.parallel.id,
            academic_year_id=self.academic_year.id,
        )
        self.reader = get_reader(self.uow, teacher_id=self.employee.id, number='12345')

        # Установим 1 день для максимального срока выдачи, чтобы создать задолженность у читателя
        self.example = get_registry_example(self.uow, max_date=1)
        self.iss_del = get_issuance_delivery(
            self.uow,
            school_id=self.school.id,
            reader_id=self.reader.id,
            example_id=self.example.id,
        )

        self.list_url = reverse('readers-list')
        self.detail_url = reverse('readers-detail', args=[self.reader.id])

    def test_list(self) -> None:
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ('count', 'next', 'previous', 'results'):
            with self.subTest(field=field):
                self.assertIn(field, response.data)
        self.assert_employee(response.json()['results'][0])

    def test_detail(self) -> None:
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_employee(response.json())

    def test_update(self) -> None:
        number = '54321'

        response = self.client.patch(self.detail_url, data={'number': number})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['number'], number)

    def test_not_allowed_methods(self) -> None:
        requests = (
            ('post', self.list_url),
            ('delete', self.detail_url),
        )

        for method, url in requests:
            with self.subTest(method=method):
                response = self.client.generic(method, url)
                self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_search_by_fields(self) -> None:
        search_fields = {
            'firstname': self.person.firstname,
            'number': self.reader.number,
            'surname': self.person.surname,
            'patronymic': self.person.patronymic,

        }

        for field, value in search_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {'search': value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertGreater(len(results), 0)
                self.assert_employee(results[0])

    def test_search_by_nonexistent_values(self) -> None:
        search_fields = {
            'firstname': 'NonExistentFirstname',
            'number': '00000',
            'surname': 'NonExistentSurname',
            'patronymic': 'NonExistentPatronymic',
        }

        for field, value in search_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {'search': value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertEqual(len(results), 0)

    def test_filter_by_fields(self) -> None:
        filter_fields = {
            'role': self.reader.role,
            'school_id': self.school.id,
            'number': self.reader.number,
            'class_year_id': self.class_year.id,
            'overdue_examples_count': 1,
        }

        for field, value in filter_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, data={field: value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertGreater(len(results), 0)
                self.assert_employee(results[0])

    def test_filter_by_nonexistent_values(self) -> None:
        filter_fields = {
            'role': ReaderRole.STUDENT.value if self.reader.role != ReaderRole.STUDENT else ReaderRole.TEACHER.value,
            'school_id': 999999,
            'number': '00000',
            'class_year_id': '00000000-0000-0000-0000-000000000000',
            'overdue_examples_count': 10,
        }

        for field, value in filter_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {field: value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']

                self.assertEqual(len(results), 0)

    def assert_employee(self, employee: dict[str, Any]) -> None:
        self.assertDictEqual(
            employee,
            {
                'id': self.reader.id,
                'number': self.reader.number,
                'role': self.reader.role.label,
                'overdue_examples_count': 1,
                'employee': {
                    'id': self.employee.id,
                    'person': {
                        'id': self.person.id,
                        'firstname': self.person.firstname,
                        'surname': self.person.surname,
                        'patronymic': self.person.patronymic,
                    },
                    'class_year': {
                        'id': self.class_year.id,
                        'name': self.class_year.name,
                    },
                    'school': {
                        'id': self.school.id,
                        'shortname': self.school.short_name,
                    },
                },
                'pupil': None,
            },
        )
