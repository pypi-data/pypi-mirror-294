from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import (
    SearchFilter,
)

from edulib.core.lib_udc.domain import (
    CreateUdc,
    DeleteUdc,
    UpdateUdc,
)
from edulib.core.lib_udc.models import (
    LibraryUDC,
)
from edulib.rest.base.viewsets import (
    CommandBasedModelViewSet,
)
from edulib.rest.udc.filters import (
    UdcFilter,
)
from edulib.rest.udc.serializers import (
    UdcSerializer,
)


class UdcViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с разделами УДК."""

    serializer_class = UdcSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = UdcFilter
    search_fields = ('code', 'name')

    create_command = CreateUdc
    update_command = UpdateUdc
    delete_command = DeleteUdc

    def get_queryset(self):
        queryset = LibraryUDC.objects.all()

        parent_id = self.request.query_params.get('parent_id')
        if parent_id:
            queryset = queryset.filter(parent=parent_id)
        else:
            queryset = queryset.filter(parent__isnull=True)

        return queryset
