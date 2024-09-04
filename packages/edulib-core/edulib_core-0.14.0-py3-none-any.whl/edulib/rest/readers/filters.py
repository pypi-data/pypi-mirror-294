from django_filters import (
    rest_framework as filters,
)

from edulib.core.persons.domain.model import (
    Person,
)
from edulib.core.readers import (
    domain,
)
from edulib.core.readers.models import (
    Reader,
)


class ReaderFilter(filters.FilterSet):
    class_year_id = filters.CharFilter(field_name='class_year_id', lookup_expr='exact')
    school_id = filters.NumberFilter(field_name='dependent_school_id', lookup_expr='exact')
    overdue_examples_count = filters.NumberFilter(field_name='overdue_examples_count', lookup_expr='exact')

    ordering = filters.OrderingFilter(
        fields=(
            ('class_year_id', 'class_year_id'),
            ('dependent_school_id', 'school_id'),
            ('firstname', 'firstname'),
            ('number', 'number'),
            ('overdue_examples_count', 'overdue_examples_count'),
            ('patronymic', 'patronymic'),
            ('role', 'role'),
            ('surname', 'surname'),
        ),
        field_labels={
            'class_year_id': 'Идентификатор класса',
            'firstname': Person.firstname.title,
            'number': domain.Reader.number.title,
            'overdue_examples_count': 'Задолженность',
            'patronymic': Person.patronymic.title,
            'role': domain.Reader.role.title,
            'school_id': 'Идентификатор школы',
            'surname': Person.surname.title,

        }
    )

    class Meta:
        model = Reader
        fields = (
            'class_year_id',
            'number',
            'role',
            'school_id',
            'overdue_examples_count',
        )
