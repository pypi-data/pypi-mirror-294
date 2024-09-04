from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import (
    SearchFilter,
)
from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
)

from edulib.core.lib_registry.models import (
    LibMarkInformProduct,
)
from edulib.rest.info_product_marks.filters import (
    InfoProductMarkFilter,
)
from edulib.rest.info_product_marks.serializers import (
    InfoProductMarkSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class InfoProductMarkViewSet(ReadOnlyModelViewSet):
    """Эндпоинты для работы  со знаками информационной продукции."""

    queryset = LibMarkInformProduct.objects.all()
    serializer_class = InfoProductMarkSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = InfoProductMarkFilter
    search_fields = ('code', 'name',)
