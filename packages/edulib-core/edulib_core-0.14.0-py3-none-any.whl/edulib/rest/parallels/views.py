from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import (
    SearchFilter,
)
from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
)

from edulib.core.parallels.models import (
    Parallel,
)
from edulib.rest.parallels.filters import (
    ParallelFilter,
)
from edulib.rest.parallels.serializers import (
    ParallelSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class ParallelsViewSet(ReadOnlyModelViewSet):
    queryset = Parallel.objects.all()
    serializer_class = ParallelSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = ParallelFilter
    search_fields = ('title',)
