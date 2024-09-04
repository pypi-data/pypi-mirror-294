from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import (
    SearchFilter,
)

from edulib.core.lib_publishings.domain.commands import (
    CreatePublishing,
    DeletePublishing,
    UpdatePublishing,
)
from edulib.core.lib_publishings.models import (
    LibraryPublishings,
)
from edulib.rest.base.viewsets import (
    CommandBasedModelViewSet,
)
from edulib.rest.publishings.filters import (
    PublishingFilter,
)
from edulib.rest.publishings.serializers import (
    PublishingSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class PublishingViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с издательствами."""

    queryset = LibraryPublishings.objects.all()
    serializer_class = PublishingSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = PublishingFilter
    search_fields = ('name',)

    create_command = CreatePublishing
    update_command = UpdatePublishing
    delete_command = DeletePublishing
