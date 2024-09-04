from django_filters import (
    rest_framework as filters,
)

from edulib.core.parallels import (
    domain,
)
from edulib.core.parallels.models import (
    Parallel,
)


class ParallelFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('title', 'title'),
        ),
        field_labels={
            'title': domain.Parallel.title.title,
        },
    )
    class Meta:
        model = Parallel
        fields = []
