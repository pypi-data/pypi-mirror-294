from django_filters import (
    rest_framework as filters,
)

from edulib.core.lib_example_types import (
    domain,
)
from edulib.core.lib_example_types.models import (
    LibraryExampleType,
)


class ExampleTypeFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
        ),
        field_labels={
            'name': domain.ExampleType.name.title,
        },
    )
    class Meta:
        model = LibraryExampleType
        fields = []
