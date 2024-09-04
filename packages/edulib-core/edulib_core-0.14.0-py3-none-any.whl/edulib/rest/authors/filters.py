from django_filters import (
    rest_framework as filters,
)

from edulib.core.lib_authors import (
    domain,
)
from edulib.core.lib_authors.models import (
    LibraryAuthors,
)


class AuthorFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
        ),
        field_labels={
            'name': domain.Author.name.title,
        }
    )

    class Meta:
        model = LibraryAuthors
        fields = []
