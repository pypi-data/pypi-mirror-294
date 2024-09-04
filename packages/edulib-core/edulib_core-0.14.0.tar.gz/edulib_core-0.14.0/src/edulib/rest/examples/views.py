from typing import (
    TYPE_CHECKING,
)

from django.db.models import (
    Exists,
    OuterRef,
    Q,
)
from django.shortcuts import (
    get_object_or_404,
)
from django.utils import (
    timezone,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework import (
    status,
)
from rest_framework.decorators import (
    action,
)
from rest_framework.filters import (
    SearchFilter,
)
from rest_framework.response import (
    Response,
)

from edulib.core import (
    bus,
)
from edulib.core.issuance_delivery.models import (
    IssuanceDelivery,
)
from edulib.core.lib_registry.domain import (
    CopyRegistryExample,
    CreateRegistryExample,
    DeleteRegistryExample,
    UpdateRegistryExample,
)
from edulib.core.lib_registry.models import (
    LibRegistryEntry,
    LibRegistryExample,
)
from edulib.rest.base.viewsets import (
    CommandBasedModelViewSet,
)
from edulib.rest.examples.filters import (
    ExampleFilter,
)
from edulib.rest.examples.serializers import (
    ExampleCopySerializer,
    ExampleListSerializer,
    ExampleRetrieveSerializer,
    ExampleSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


if TYPE_CHECKING:
    from rest_framework.serializers import (
        Serializer,
    )


class RegistryExampleViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с экземплярами библиотечных изданий."""

    queryset = LibRegistryExample.objects.none()
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('card_number',)
    filterset_class = ExampleFilter

    create_command = CreateRegistryExample
    update_command = UpdateRegistryExample
    delete_command = DeleteRegistryExample

    def get_queryset(self):
        registry_entry = get_object_or_404(LibRegistryEntry, pk=self.kwargs.get('registryentry_id'))

        return (
            registry_entry.examples.select_related('publishing')
            .annotate(
                occupied=Exists(
                    IssuanceDelivery.objects.filter(
                        Q(fact_delivery_date__isnull=True) | Q(fact_delivery_date__gt=timezone.now()),
                        example=OuterRef('pk'),
                    )
                ),
            )
            .all()
        )

    def get_serializer_class(self) -> type['Serializer']:
        if self.action == 'list':
            return ExampleListSerializer
        if self.action == 'retrieve':
            return ExampleRetrieveSerializer
        if self.action == 'copy':
            return ExampleCopySerializer

        return ExampleSerializer

    def prepare_additional_create_command_data(self, request, *args, **kwargs):
        return {
            'lib_reg_entry_id': kwargs.get('registryentry_id'),
        }

    @action(detail=True, methods=['post'])
    def copy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        command = CopyRegistryExample(id=kwargs.get(self.lookup_field), **serializer.validated_data)

        result = bus.handle(command)

        return Response(data=self.get_serializer(result).data, status=status.HTTP_201_CREATED)
