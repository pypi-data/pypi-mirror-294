from django_filters import (
    rest_framework as filters,
)

from edulib.core.lib_registry.domain import (
    RegistryEntry,
    RegistryExample,
)
from edulib.core.lib_registry.models import (
    LibRegistryEntry,
)


_ordering_fields = (
    ('status', 'status'),
    ('title', 'title'),
    ('author__name', 'author__name'),
    ('type__name', 'type__name'),
    ('discipline_name', 'discipline_name'),
    ('udc__code', 'udc__code'),
    ('bbc__code', 'bbc__code'),
    ('count', 'count'),
    ('free_count', 'free_count'),
)
_ordering_field_labels = {
    'status': RegistryEntry.status.title,
    'title': RegistryEntry.title.title,
    'author__name': RegistryEntry.author_id.title,
    'type__name': RegistryEntry.type_id.title,
    'discipline_name': RegistryEntry.discipline_id.title,
    'udc__code': RegistryEntry.udc_id.title,
    'bbc__code': RegistryEntry.bbc_id.title,
    'count': 'Общее количество экземпляров',
    'free_count': 'Количество свободных экземпляров',
}


class EntryFilter(filters.FilterSet):
    author_id = filters.NumberFilter(label=RegistryEntry.author_id.title)
    parallel_id = filters.CharFilter(field_name='parallels', lookup_expr='in', label='Параллель')
    type_id = filters.NumberFilter(label=RegistryEntry.type_id.title)
    publishing_id = filters.CharFilter(
        field_name='examples__publishing_id',
        lookup_expr='in',
        label=RegistryExample.publishing_id.title,
    )
    edition_year = filters.NumberFilter(
        field_name='examples__edition_year',
        lookup_expr='exact',
        label=RegistryExample.edition_year.title,
    )
    discipline_id = filters.NumberFilter(label=RegistryEntry.discipline_id.title)

    ordering = filters.OrderingFilter(
        fields=_ordering_fields,
        field_labels=_ordering_field_labels,
    )

    class Meta:
        model = LibRegistryEntry
        fields = ('status',)


class GeneralFundFilter(EntryFilter):
    municipal_unit = filters.CharFilter(field_name='municipal_unit_name', lookup_expr='icontains')
    school = filters.CharFilter(field_name='school_name', lookup_expr='icontains')
    count = filters.NumberFilter(field_name='count')
    free_count = filters.NumberFilter(field_name='free_count')
    lack = filters.NumberFilter(field_name='lack')
    excess = filters.NumberFilter(field_name='excess')
    sufficiency = filters.NumberFilter(field_name='sufficiency')

    ordering = filters.OrderingFilter(
        fields=(
            *_ordering_fields,
            ('municipal_unit_name', 'municipal_unit_name'),
            ('school_name', 'school_name'),
            ('publishings', 'publishings'),
            ('lack', 'lack'),
            ('excess', 'excess'),
            ('sufficiency', 'sufficiency'),
        ),
        field_labels={
            **_ordering_field_labels,
            'municipal_unit_name': 'Муниципальная единица',
            'school_name': 'Организация',
            'publishings': 'Издательства',
            'lack': 'Недостаток',
            'excess': 'Излишек',
            'sufficiency': 'Обеспеченность',
        },
    )
