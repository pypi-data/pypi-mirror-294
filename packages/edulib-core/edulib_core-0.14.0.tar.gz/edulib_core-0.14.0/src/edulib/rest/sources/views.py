from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import (
    SearchFilter,
)

from edulib.core.lib_sources.domain.commands import (
    CreateSource,
    DeleteSource,
    UpdateSource,
)
from edulib.core.lib_sources.models import (
    LibrarySource,
)
from edulib.rest.base.viewsets import (
    CommandBasedModelViewSet,
)
from edulib.rest.sources.filters import (
    SourceFilter,
)
from edulib.rest.sources.serializers import (
    SourceSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class SourceViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с источниками поступления."""

    queryset = LibrarySource.objects.all()
    serializer_class = SourceSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = SourceFilter
    search_fields = ('name',)

    create_command = CreateSource
    update_command = UpdateSource
    delete_command = DeleteSource
