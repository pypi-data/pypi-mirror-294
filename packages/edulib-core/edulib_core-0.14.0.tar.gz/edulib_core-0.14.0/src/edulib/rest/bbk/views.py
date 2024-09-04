from django_filters.rest_framework import (
    DjangoFilterBackend,
)

from edulib.core.directory.domain import (
    CreateBbk,
    DeleteBbk,
    UpdateBbk,
)
from edulib.core.directory.models import (
    Catalog,
)
from edulib.rest.base.viewsets import (
    CommandBasedModelViewSet,
)
from edulib.rest.bbk.filters import (
    BbkFilter,
)
from edulib.rest.bbk.serializers import (
    BbkDisplaySerializer,
    BbkSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class BbkViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с разделами ББК."""

    queryset = Catalog.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = BbkFilter

    create_command = CreateBbk
    update_command = UpdateBbk
    delete_command = DeleteBbk

    def get_serializer_class(self):
        serializer_class = BbkDisplaySerializer
        if self.action in ['create', 'update', 'partial_update']:
            serializer_class = BbkSerializer

        return serializer_class
