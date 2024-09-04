from django_filters import (
    rest_framework as filters,
)

from edulib.core.employees import (
    domain,
)
from edulib.core.employees.models import (
    Employee,
)
from edulib.core.persons.domain import (
    Person,
)
from edulib.core.schools.domain import (
    School,
)


class EmployeeFilter(filters.FilterSet):
    job_names = filters.CharFilter(
        lookup_expr='icontains',
        label=domain.Employee.job_name.title
    )
    firstname = filters.CharFilter(
        lookup_expr='icontains',
        label=Person.firstname.title,
        field_name='person__firstname',
    )
    surname = filters.CharFilter(
        lookup_expr='icontains',
        label=Person.surname.title,
        field_name='person__surname',
    )
    patronymic = filters.CharFilter(
        lookup_expr='icontains',
        label=Person.patronymic.title,
        field_name='person__patronymic',
    )
    date_of_birth = filters.DateFilter(
        lookup_expr='exact',
        label=Person.date_of_birth.title,
        field_name='person__date_of_birth',
    )

    ordering = filters.OrderingFilter(
        fields=(
            ('school_id', 'school_id'),
            ('school__short_name', 'school__short_name'),
            ('job_names', 'job_names'),
            ('person__surname', 'surname'),
            ('person__firstname', 'firstname'),
            ('person__patronymic', 'patronymic'),
            ('person__date_of_birth', 'date_of_birth'),
        ),
        field_labels={
            'school_id': domain.Employee.school_id.title,
            'school__short_name': School.short_name.title,
            'job_names': domain.Employee.job_name.title,
            'person__surname': Person.surname.title,
            'person__firstname': Person.firstname.title,
            'person__patronymic': Person.patronymic.title,
            'person__date_of_birth': Person.date_of_birth.title,
        },
    )

    class Meta:
        model = Employee
        fields = (
            'school_id',
        )
