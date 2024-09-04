from typing import (
    TYPE_CHECKING,
)

from rest_framework import (
    serializers,
)

from edulib.core.lib_registry import (
    domain,
)
from edulib.core.lib_registry.models import (
    LibRegistryExample,
)
from edulib.rest.publishings.serializers import (
    PublishingSerializer,
)


if TYPE_CHECKING:
    from collections import (
        OrderedDict,
    )


class BaseExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibRegistryExample
        fields = (
            'id',
            'card_number',
            'inflow_date',
            'edition',
            'edition_year',
            'invoice_number',
            # TODO: https://jira.bars.group/browse/EDUBOOKS-92 добавить акт списания
            # 'writeoff_act',
        )


class ExampleListSerializer(BaseExampleSerializer):
    publishing = PublishingSerializer(label=domain.RegistryExample.publishing_id.title)
    occupied = serializers.BooleanField()

    class Meta(BaseExampleSerializer.Meta):
        fields = (
            *BaseExampleSerializer.Meta.fields,
            'publishing',
            'occupied',
        )


class ExampleRetrieveSerializer(BaseExampleSerializer):
    publishing = PublishingSerializer(label=domain.RegistryExample.publishing_id.title)
    occupied = serializers.BooleanField()

    class Meta(BaseExampleSerializer.Meta):
        fields = (
            *BaseExampleSerializer.Meta.fields,
            'publishing',
            'occupied',
            'edition_place',
            'duration',
            'book_code',
            'price',
            'max_date',
            'fin_source',
        )

    def to_representation(self, instance: LibRegistryExample) -> 'OrderedDict':
        instance.fin_source = instance.get_fin_source_display()

        return super().to_representation(instance)


class ExampleSerializer(BaseExampleSerializer):
    publishing_id = serializers.IntegerField(label=domain.RegistryExample.publishing_id.title, required=False)

    class Meta(BaseExampleSerializer.Meta):
        model = LibRegistryExample
        fields = (
            *BaseExampleSerializer.Meta.fields,
            'publishing_id',
            'edition_place',
            'duration',
            'book_code',
            'price',
            'max_date',
            'fin_source',
        )


class ExampleCopySerializer(serializers.Serializer):  # pylint: disable=abstract-method
    count_for_copy = serializers.IntegerField(label='Количество копий', min_value=1)
