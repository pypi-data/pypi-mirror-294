from django_filters import (
    rest_framework as filters,
)

from edulib.core.issuance_delivery import (
    domain,
)
from edulib.core.issuance_delivery.models import (
    IssuanceDelivery,
)
from edulib.core.lib_registry.domain.model import (
    RegistryEntry,
    RegistryExample,
)


class IssuanceDeliveryFilter(filters.FilterSet):
    author_name = filters.CharFilter(field_name='example__lib_reg_entry__author__name', lookup_expr='icontains')
    example_id = filters.NumberFilter(field_name='example_id', lookup_expr='exact')
    example_title = filters.CharFilter(field_name='example__lib_reg_entry__title', lookup_expr='icontains')
    plan_del_date = filters.DateFilter(field_name='plan_del_date', lookup_expr='exact')
    reader_id = filters.NumberFilter(field_name='reader_id', lookup_expr='exact')

    ordering = filters.OrderingFilter(
        fields=(
            ('example__lib_reg_entry__title', 'example__lib_reg_entry__title'),
            ('example__lib_reg_entry__author__name', 'example__lib_reg_entry__author__name'),
            ('example__card_number', 'example__card_number'),
            ('example__max_date', 'example__max_date'),
            ('extension_days_count', 'extension_days_count'),
            ('issuance_date', 'issuance_date'),
            ('plan_del_date', 'plan_del_date'),
        ),
        field_labels={
            'example__lib_reg_entry__title': RegistryEntry.title.title,
            'example__lib_reg_entry__author__name': RegistryEntry.author_id.title,
            'example__card_number': RegistryExample.card_number.title,
            'example__max_date': RegistryExample.max_date.title,
            'extension_days_count': domain.IssuanceDelivery.extension_days_count.title,
            'issuance_date': domain.IssuanceDelivery.issuance_date.title,
            'plan_del_date': 'Плановая дата сдачи',
        },
    )

    class Meta:
        model = IssuanceDelivery
        fields = (
            'fact_delivery_date',
        )
