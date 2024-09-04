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
from edulib.core.address.tests.utils import (
    get_address,
)
from edulib.core.employees.tests.utils import (
    get_employee,
)
from edulib.core.genders.tests.utils import (
    get_gender,
)
from edulib.core.persons.tests.utils import (
    get_person,
)
from edulib.core.schools.tests.utils import (
    get_school,
)


class EmployeeRestTestCase(APITransactionTestCase):
    """Тесты справочника "Сотрудники"."""

    def setUp(self) -> None:
        self.uow = bus.get_uow()

        self.gender = get_gender(self.uow)
        self.person = get_person(self.uow, gender_id=self.gender.id, email='test@mail.ru', snils='001-001-997 12')

        self.address = get_address(self.uow)
        self.person.temp_reg_addr_id = self.address.id
        self.uow.persons.update(self.person)

        self.school = get_school(self.uow)
        self.employee = get_employee(self.uow, person_id=self.person.id, school_id=self.school.id)

        self.list_url = reverse('employees-list')
        self.detail_url = reverse('employees-detail', args=[self.employee.id])

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

    def test_not_allowed_methods(self) -> None:
        requests = (
            ('post', self.list_url),
            ('put', self.detail_url),
            ('patch', self.detail_url),
            ('delete', self.detail_url),
        )

        for method, url in requests:
            with self.subTest(method=method):
                response = self.client.generic(method, url)
                self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_search_by_fields(self) -> None:
        search_fields = {
            'firstname': self.person.firstname,
            'patronymic': self.person.patronymic,
            'surname': self.person.surname,
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
            'patronymic': 'NonExistentPatronymic',
            'surname': 'NonExistentSurname',
        }

        for field, value in search_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {'search': value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertEqual(len(results), 0)

    def test_filter_by_fields(self) -> None:
        filter_fields = {
            'school_id': self.school.id,
            'job_names': self.employee.job_name,
            'firstname': self.person.firstname,
            'surname': self.person.surname,
            'patronymic': self.person.patronymic,
            'date_of_birth': str(self.person.date_of_birth),
        }

        for field, value in filter_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {field: value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertGreater(len(results), 0)
                self.assert_employee(results[0])

    def test_filter_by_nonexistent_values(self) -> None:
        filter_fields = {
            'school_id': 999999,
            'job_names': 'NonExistentJobName',
            'firstname': 'NonExistentFirstname',
            'surname': 'NonExistentSurname',
            'patronymic': 'NonExistentPatronymic',
            'date_of_birth': '1900-01-01',
        }

        for field, value in filter_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {field: value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertEqual(len(results), 0)

    def assert_employee(self, response: dict[str, Any]) -> None:
        self.assertDictEqual(
            response,
            {
                'id': self.employee.id,
                'surname': self.person.surname,
                'firstname': self.person.firstname,
                'patronymic': self.person.patronymic,
                'date_of_birth': str(self.person.date_of_birth),
                'school': {
                    'id': self.school.id,
                    'short_name': self.school.short_name,
                },
                'job_names': [self.employee.job_name, ],
                'gender': {
                    'id': self.gender.id,
                    'name': self.gender.name,
                },
                'inn': self.person.inn,
                'telephone': self.person.phone,
                'email': self.person.email,
                'snils': self.person.snils,
                'temp_reg_addr': {
                    'id': self.address.id,
                    'full_address': self.address.full,
                },
                'person_id': self.person.id,
            },
        )
