from django.db.models import (
    IntegerField,
    Value,
)
from django.db.models.functions import (
    Cast,
    Replace,
)
from django_filters import (
    rest_framework as filters,
)

from edulib.core.lib_registry import (
    domain,
)
from edulib.core.lib_registry.models import (
    LibMarkInformProduct,
)


class InfoProductMarkFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('code', 'code'),
        ),
        field_labels={
            'name': domain.InfoProductMark.name.title,
            'code': domain.InfoProductMark.code.title,
        },
    )

    class Meta:
        model = LibMarkInformProduct
        fields = ['name', 'code']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        # Заменяем "+" на пустую строку и сортируем по числовому значению
        if 'code' in self.data.get('ordering', ''):
            direction = '-' if self.data['ordering'].startswith('-') else ''
            queryset = queryset.annotate(
                code_as_number=Cast(
                    Replace('code', Value('+'), Value('')), IntegerField()
                )
            ).order_by(f'{direction}code_as_number')
        return queryset
