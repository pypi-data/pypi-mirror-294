from django_filters import (
    rest_framework as filters,
)

from edulib.core.schools import (
    domain,
)
from edulib.core.schools.models import (
    School,
)


class SchoolFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('short_name', 'short_name'),
            ('institution_type_id', 'institution_type_id'),
        ),
        field_labels={
            'name': domain.School.name.title,
            'short_name': domain.School.short_name.title,
            'institution_type_id': domain.School.institution_type_id.title,
        },
    )

    class Meta:
        model = School
        fields = []
