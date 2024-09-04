from django_filters import (
    rest_framework as filters,
)

from edulib.core.lib_registry.domain.model import (
    RegistryExample,
)
from edulib.core.lib_registry.models import (
    LibRegistryExample,
)


class ExampleFilter(filters.FilterSet):
    publishing = filters.CharFilter(
        field_name='publishing__name',
        lookup_expr='icontains',
        label=RegistryExample.publishing_id.title,
    )
    edition = filters.CharFilter(field_name='edition', lookup_expr='icontains', label=RegistryExample.edition.title)
    occupied = filters.BooleanFilter(field_name='occupied', lookup_expr='exact', label='Занятость')

    ordering = filters.OrderingFilter(
        fields=(
            ('card_number', 'card_number'),
            ('inflow_date', 'inflow_date'),
            ('edition', 'edition'),
            ('edition_year', 'edition_year'),
            ('publishing__name', 'publishing__name'),
            ('occupied', 'occupied'),
            # TODO: https://jira.bars.group/browse/EDUBOOKS-92 добавить акт списания
            # ('writeoff_act__date', 'writeoff_act__date'),
            # ('writeoff_act__act_number', 'writeoff_act__act_number'),
        ),
        field_labels={
            'card_number': RegistryExample.card_number.title,
            'inflow_date': RegistryExample.inflow_date.title,
            'edition': RegistryExample.edition.title,
            'edition_year': RegistryExample.edition_year.title,
            'publishing__name': RegistryExample.publishing_id.title,
            'occupied': 'Занятость',
        },
    )

    class Meta:
        model = LibRegistryExample
        fields = (
            'edition_year',
            'inflow_date',
        )
