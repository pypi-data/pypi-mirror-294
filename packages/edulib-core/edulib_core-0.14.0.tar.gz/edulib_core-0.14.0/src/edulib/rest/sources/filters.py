from django_filters import (
    rest_framework as filters,
)

from edulib.core.lib_sources import (
    domain,
)
from edulib.core.lib_sources.models import (
    LibrarySource,
)


class SourceFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
        ),
        field_labels={
            'name': domain.Source.name.title,
        },
    )

    class Meta:
        model = LibrarySource
        fields = []
