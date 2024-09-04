from django_filters import (
    rest_framework as filters,
)

from edulib.core.lib_passport import (
    domain,
)
from edulib.core.lib_passport.models import (
    LibPassport,
)


class PassportFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
        ),
        field_labels={
            'name': domain.Passport.name.title,
        },
    )

    class Meta:
        model = LibPassport
        fields = []
