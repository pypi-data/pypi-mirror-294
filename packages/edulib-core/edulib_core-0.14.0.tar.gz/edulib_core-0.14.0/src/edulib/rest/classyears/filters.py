from django.db.models import (
    Func,
    Value,
)
from django_filters import (
    rest_framework as filters,
)

from edulib.core.academic_years.domain import (
    AcademicYear,
)
from edulib.core.classyears import (
    domain,
)
from edulib.core.classyears.models import (
    ClassYear,
)
from edulib.core.persons.domain import (
    Person,
)


class ClassYearFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('school_id', 'school_id'),
            ('teacher__surname', 'teacher__surname'),
            ('teacher__firstname', 'teacher__firstname'),
            ('teacher__patronymic', 'teacher__patronymic'),
            ('academic_year__name', 'academic_year__name'),
        ),
        field_labels={
            'name': domain.ClassYear.name.title,
            'school_id': domain.ClassYear.school_id.title,
            'teacher__surname': Person.surname.title,
            'teacher__firstname': Person.firstname.title,
            'teacher__patronymic': Person.patronymic.title,
            'academic_year__name': AcademicYear.name.title,
        },
    )
    teacher__fullname = filters.CharFilter(method='filter_fullname', label='ФИО учителя')
    letter = filters.CharFilter(lookup_expr='iexact', label=domain.ClassYear.letter.title)

    def filter_fullname(self, queryset, name, value):
        return queryset.annotate(
            fullname=Func(
                Value(' '),
                'teacher__surname',
                'teacher__firstname',
                'teacher__patronymic',
                function='concat_ws',
            )
        ).filter(fullname__icontains=value)

    class Meta:
        model = ClassYear
        fields = (
            'parallel_id',
            'academic_year_id',
            'school_id',
        )
