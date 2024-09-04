from django_filters import (
    rest_framework as filters,
)

from edulib.core.disciplines import (
    domain,
)
from edulib.core.disciplines.models import (
    Discipline,
)


class DisciplineFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
        ),
        field_labels={
            'name': domain.Discipline.name.title,
        },
    )

    class Meta:
        model = Discipline
        fields = ('name',)
