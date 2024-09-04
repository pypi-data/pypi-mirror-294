from django.db.models import (
    OuterRef,
    Q,
    Subquery,
)
from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from rest_framework.filters import (
    SearchFilter,
)
from rest_framework.viewsets import (
    ReadOnlyModelViewSet,
)

from edulib.core.address.models import (
    Address,
)
from edulib.core.institution_types.models import (
    InstitutionType,
)
from edulib.core.schools.models import (
    School,
)
from edulib.rest.schools.filters import (
    SchoolFilter,
)
from edulib.rest.schools.serializers import (
    SchoolSerializer,
)
from edulib.rest.utils.pagination import (
    LimitOffsetPagination,
)


class SchoolViewSet(ReadOnlyModelViewSet):
    """Эндпоинты для работы с организациями."""

    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filterset_class = SchoolFilter
    search_fields = ('name', 'short_name', 'institution_type_id')

    def get_queryset(self):
        institution_type_query = InstitutionType.objects.filter(id=OuterRef('institution_type_id')).values('name')
        address_query = Address.objects.filter(
            Q(id=OuterRef('f_address_id')) | Q(id=OuterRef('u_address_id'))
        )
        return School.objects.annotate(
            institution_type_name=institution_type_query.values('name'),
            f_address_name=Subquery(
                address_query.filter(id=OuterRef('f_address_id')).values('full')[:1]
            ),
            u_address_name=Subquery(
                address_query.filter(id=OuterRef('u_address_id')).values('full')[:1]
            )
        )
