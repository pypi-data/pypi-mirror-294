from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import (
    SearchFilter,
)

from edulib.core.lib_example_types.domain.commands import (
    CreateExampleType,
    DeleteExampleType,
    UpdateExampleType,
)
from edulib.core.lib_example_types.models import (
    LibraryExampleType,
)
from edulib.rest.base.viewsets import (
    CommandBasedModelViewSet,
)
from edulib.rest.example_types.filters import (
    ExampleTypeFilter,
)
from edulib.rest.example_types.serializers import (
    ExampleTypeSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class ExampleTypeViewSet(CommandBasedModelViewSet):
    """Эндпоинты для работы с типами библиотечных экземпляров."""

    queryset = LibraryExampleType.objects.all()
    serializer_class = ExampleTypeSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = ExampleTypeFilter
    search_fields = ('name',)

    create_command = CreateExampleType
    update_command = UpdateExampleType
    delete_command = DeleteExampleType
