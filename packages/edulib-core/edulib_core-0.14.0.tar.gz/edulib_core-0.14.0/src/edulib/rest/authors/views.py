from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import (
    SearchFilter,
)

from edulib.core.lib_authors.domain.commands import (
    CreateAuthor,
    DeleteAuthor,
    UpdateAuthor,
)
from edulib.core.lib_authors.models import (
    LibraryAuthors,
)
from edulib.rest.authors import (
    serializers,
)
from edulib.rest.authors.filters import (
    AuthorFilter,
)
from edulib.rest.base.viewsets import (
    CommandBasedModelViewSet,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class AuthorViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с авторами."""

    queryset = LibraryAuthors.objects.all()
    serializer_class = serializers.AuthorSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = AuthorFilter
    search_fields = ('name',)

    create_command = CreateAuthor
    update_command = UpdateAuthor
    delete_command = DeleteAuthor
