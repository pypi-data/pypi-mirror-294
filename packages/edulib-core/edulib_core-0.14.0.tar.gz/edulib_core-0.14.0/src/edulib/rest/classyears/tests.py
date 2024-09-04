from django.urls import (
    reverse,
)
from rest_framework import (
    status,
)
from rest_framework.test import (
    APITransactionTestCase,
)
from traitlets import (
    Any,
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
from edulib.core.parallels.tests.utils import (
    get_parallel,
)
from edulib.core.persons.tests.utils import (
    get_person,
)
from edulib.core.schools.tests.utils import (
    get_school,
)


class ClassYearRestTestCase(APITransactionTestCase):
    """Тесты справочника "Классы"."""

    def setUp(self) -> None:
        self.uow = bus.get_uow()

        self.school = get_school(self.uow)
        self.person = get_person(self.uow)
        self.employee = get_employee(self.uow, school_id=self.school.id, person_id=self.person.id)
        self.academic_year = get_academic_year(self.uow)
        self.parallel = get_parallel(self.uow)

        self.classyear = get_class_year(
            self.uow,
            school_id=self.school.id,
            teacher_id=self.employee.id,
            parallel_id=self.parallel.id,
            academic_year_id=self.academic_year.id,
        )

        self.list_url = reverse('classyears-list')
        self.detail_url = reverse('classyears-detail', args=[self.classyear.id])

    def test_list(self) -> None:
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ('count', 'next', 'previous', 'results'):
            with self.subTest(field=field):
                self.assertIn(field, response.data)
        self.assert_classyear(response.json()['results'][0])

    def test_detail(self) -> None:
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_classyear(response.json())

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

    def assert_classyear(self, response: dict[str, Any]) -> None:
        self.assertDictEqual(
            response,
            {
                'id': self.classyear.id,
                'name': self.classyear.name,
                'school': {
                    'id': self.school.id,
                    'short_name': self.school.short_name,
                },
                'teacher': {
                    'id': self.employee.id,
                    'surname': self.person.surname,
                    'firstname': self.person.firstname,
                    'patronymic': self.person.patronymic,
                },
                'academic_year': {
                    'id': self.academic_year.id,
                    'name': self.academic_year.name,
                },
                'parallel': {
                    'id': self.parallel.id,
                    'title': self.parallel.title,
                },
            },
        )
