from django_filters import (
    rest_framework as filters,
)

from edulib.core.lib_udc import (
    domain,
)
from edulib.core.lib_udc.models import (
    LibraryUDC,
)


class UdcFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('code', 'code'),
        ),
        field_labels={
            'code': domain.Udc.code.title,
        },
    )

    class Meta:
        model = LibraryUDC
        fields = []
