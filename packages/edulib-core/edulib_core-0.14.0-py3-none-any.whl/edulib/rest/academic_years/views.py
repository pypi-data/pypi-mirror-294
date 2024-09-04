from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import (
    SearchFilter,
)
from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
)

from edulib.core.academic_years.models import (
    AcademicYear,
)
from edulib.rest.academic_years.filters import (
    AcademicYearFilter,
)
from edulib.rest.academic_years.serializers import (
    AcademicYearSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class AcademicYearViewSet(ReadOnlyModelViewSet):
    """Эндпоинты для работы с периодами обучения (учебными годами)."""

    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = AcademicYearFilter
    search_fields = ('code', 'name', 'date_begin', 'date_end')
