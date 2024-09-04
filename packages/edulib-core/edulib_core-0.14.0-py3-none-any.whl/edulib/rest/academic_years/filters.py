from django_filters import (
    rest_framework as filters,
)

from edulib.core.academic_years import (
    domain,
)
from edulib.core.academic_years.models import (
    AcademicYear,
)


class AcademicYearFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('code', 'code'),
            ('name', 'name'),
            ('date_begin', 'date_begin'),
            ('date_end', 'date_end'),
        ),
        field_labels={
            'code': domain.AcademicYear.code.title,
            'name': domain.AcademicYear.name.title,
            'date_begin': domain.AcademicYear.date_begin.title,
            'date_end': domain.AcademicYear.date_end.title,
        }
    )

    class Meta:
        model = AcademicYear
        fields = []
