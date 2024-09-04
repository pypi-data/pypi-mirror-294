from typing import (
    Any,
)
from uuid import (
    uuid4,
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

from edulib.core.classyears.models import (
    ClassYear,
)
from edulib.core.genders.models import (
    Gender,
)
from edulib.core.persons.models import (
    Person,
)
from edulib.core.pupils.models import (
    Pupil,
)
from edulib.core.schoolchildren.models import (
    Schoolchild,
)
from edulib.core.schools.models import (
    School,
)


class SchoolchildRestTests(APITransactionTestCase):
    """Тесты для эндпоинтов учащихся школы."""

    @staticmethod
    def create_schoolchild(person, **kwargs):
        fields = {
            'person_id': person.id,
        } | kwargs
        return Schoolchild.objects.create(**fields)

    @staticmethod
    def create_pupil(schoolchild, class_year, school, **kwargs):
        fields = {
            'id': uuid4(),
            'schoolchild_id': schoolchild.id,
            'class_year_id': class_year.id,
            'school_id': school.id,
            'training_begin_date': '2020-09-01',
        } | kwargs
        return Pupil.objects.create(**fields)

    def setUp(self) -> None:
        self.school = School.objects.create(id=1, short_name='МОУ СОШ №7', status=True)
        self.gender = Gender.objects.create(id=1, name='Мужской')
        self.class_year = ClassYear.objects.create(
            id=uuid4(),
            name='9A',
            school_id=self.school.id,
            parallel_id=1,
            academic_year_id=1
        )
        self.person = Person.objects.create(
            id=uuid4(),
            surname='Иванов',
            firstname='Иван',
            patronymic='Иванович',
            date_of_birth='2010-08-10',
            gender_id=self.gender.id
        )
        self.schoolchild = self.create_schoolchild(self.person)
        self.pupil = self.create_pupil(
            self.schoolchild,
            self.class_year,
            self.school
        )

        self.list_url = reverse('schoolchildren-list')
        self.detail_url = reverse('schoolchildren-detail', args=[self.schoolchild.id])

    def test_list(self) -> None:
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ('count', 'next', 'previous', 'results'):
            with self.subTest(field=field):
                self.assertIn(field, response.data)
        self.assert_schoolchildren(response.json()['results'][0])

    def test_detail(self) -> None:
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_schoolchildren(response.json())

    def assert_schoolchildren(self, schoolchild: dict[str, Any]) -> None:
        self.assertDictEqual(
            schoolchild,
            {
                'id': self.schoolchild.id,
                'person': {
                    'id': str(self.person.id),
                    'surname': self.person.surname,
                    'firstname': self.person.firstname,
                    'patronymic': self.person.patronymic,
                    'date_of_birth': str(self.person.date_of_birth),
                    'gender': {
                        'id': self.gender.id,
                        'name': self.gender.name,
                    }
                },
                'pupil': {
                    'id': str(self.pupil.id),
                    'class_year': {
                        'id': str(self.class_year.id),
                        'name': self.class_year.name,
                    },
                    'school': {
                        'id': self.school.id,
                        'short_name': self.school.short_name,
                    },
                    'training_begin_date': str(self.pupil.training_begin_date),
                    'training_end_date': self.pupil.training_end_date,
                }
            },
        )
