from django_filters import (
    rest_framework as filters,
)

from edulib.core.lib_publishings import (
    domain,
)
from edulib.core.lib_publishings.models import (
    LibraryPublishings,
)


class PublishingFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
        ),
        field_labels={
            'name': domain.Publishing.name.title,
        },
    )

    class Meta:
        model = LibraryPublishings
        fields = []
