from django_filters import (
    rest_framework as filters,
)

from edulib.core.classyears.domain import (
    ClassYear,
)
from edulib.core.genders.domain import (
    Gender,
)
from edulib.core.persons.domain import (
    Person,
)
from edulib.core.schoolchildren.models import (
    Schoolchild,
)
from edulib.core.schools.domain import (
    School,
)


class SchoolchildFilter(filters.FilterSet):
    firstname = filters.CharFilter(field_name='person_firstname', lookup_expr='icontains')
    surname = filters.CharFilter(field_name='person_surname', lookup_expr='icontains')
    patronymic = filters.CharFilter(field_name='person_patronymic', lookup_expr='icontains')
    date_of_birth = filters.DateFilter(field_name='person_date_of_birth')
    gender_id = filters.NumberFilter(field_name='person_gender_id')

    ordering = filters.OrderingFilter(
        fields=(
            ('person_firstname', 'firstname'),
            ('person_surname', 'surname'),
            ('person_patronymic', 'patronymic'),
            ('person_date_of_birth', 'date_of_birth'),
            ('person_gender_name', 'gender_name'),
            ('pupil_school_short_name', 'school_short_name'),
            ('pupil_class_year_name', 'class_year_name')
        ),
        field_labels={
            'person_firstname': Person.firstname.title,
            'person_surname': Person.surname.title,
            'person_patronymic': Person.patronymic.title,
            'person_date_of_birth': Person.date_of_birth.title,
            'person_gender_name': Gender.name.title,
            'pupil_school_short_name': School.short_name.title,
            'pupil_class_year_name': ClassYear.name.title
        }
    )

    class Meta:
        model = Schoolchild
        fields = ['firstname', 'surname', 'patronymic', 'date_of_birth', 'gender_id']
