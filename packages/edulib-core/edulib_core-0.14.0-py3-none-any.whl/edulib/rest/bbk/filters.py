from django.db.models import (
    Q,
)
from django_filters import (
    rest_framework as filters,
)

from edulib.core.directory import (
    domain,
)
from edulib.core.directory.models import (
    Catalog,
)


class BbkFilter(filters.FilterSet):
    code = filters.CharFilter(field_name='code', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    parent_id = filters.NumberFilter(field_name='parent_id', method='filter_by_parent_id')
    search = filters.CharFilter(method='search_filter')

    ordering = filters.OrderingFilter(
        fields=(
            ('code', 'code'),
        ),
        field_labels={
            'code': domain.Bbk.code.title,
        }
    )

    class Meta:
        model = Catalog
        fields = []

    def filter_by_parent_id(self, queryset, name, value):
        if value == 0:
            # Если передан 0, фильтруем по parent__isnull=True
            queryset = queryset.filter(parent__isnull=True)
        else:
            queryset = queryset.filter(parent_id=value)

        return queryset

    def search_filter(self, queryset, name, value):
        queryset = queryset.filter(Q(code__icontains=value) | Q(name__icontains=value))

        return queryset.get_ancestors(include_self=True).distinct()
