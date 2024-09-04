from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import (
    SearchFilter,
)
from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
)

from edulib.core.disciplines.models import (
    Discipline,
)
from edulib.rest.disciplines.filters import (
    DisciplineFilter,
)
from edulib.rest.disciplines.serializers import (
    DisciplineSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class DisciplineViewSet(ReadOnlyModelViewSet):
    """Эндпоинты для работы с предметами."""

    queryset = Discipline.objects.all()
    serializer_class = DisciplineSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = DisciplineFilter
    search_fields = ('name',)
