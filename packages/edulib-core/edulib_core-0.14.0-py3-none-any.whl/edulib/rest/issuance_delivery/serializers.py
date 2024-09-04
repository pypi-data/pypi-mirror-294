# pylint: disable=abstract-method
from rest_framework import (
    serializers,
)

from edulib.core.issuance_delivery import (
    domain,
)
from edulib.core.issuance_delivery.models import (
    IssuanceDelivery,
)
from edulib.core.lib_registry.domain import (
    RegistryEntry,
)
from edulib.core.lib_registry.models import (
    LibRegistryExample,
)
from edulib.core.persons.domain import (
    Person,
)
from edulib.core.readers.domain import (
    Reader,
)
from edulib.rest.authors.serializers import (
    AuthorSerializer,
)


class IssuanceDeliveryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssuanceDelivery
        fields = (
            'id',
            'issuance_date',
            'fact_delivery_date',
            'special_notes',
            'extension_days_count',
        )


class IssuanceDeliveryOutputSerializer(IssuanceDeliveryBaseSerializer):
    class Meta(IssuanceDeliveryBaseSerializer.Meta):
        fields = (
            *IssuanceDeliveryBaseSerializer.Meta.fields,
            'reader_id',
            'example_id',
        )


class IssuanceReaderSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='reader_id')
    number = serializers.CharField(source='reader.number', label=Reader.number.title)
    firstname = serializers.CharField(label=Person.firstname.title)
    surname = serializers.CharField(label=Person.surname.title)
    patronymic = serializers.CharField(label=Person.patronymic.title)


class IssuanceExampleSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='lib_reg_entry.title', label=RegistryEntry.title.title)
    author = AuthorSerializer(source='lib_reg_entry.author', label=RegistryEntry.author_id.title)

    class Meta:
        model = LibRegistryExample
        fields = (
            'id',
            'title',
            'author',
            'card_number',
            'max_date',
        )


class IssuanceDeliverySerializer(IssuanceDeliveryBaseSerializer):
    reader = IssuanceReaderSerializer(source='*', label=domain.IssuanceDelivery.reader_id.title)
    example = IssuanceExampleSerializer(label=domain.IssuanceDelivery.example_id.title)
    plan_del_date = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta(IssuanceDeliveryBaseSerializer.Meta):
        fields = (
            *IssuanceDeliveryBaseSerializer.Meta.fields,
            'reader',
            'example',
            'plan_del_date',
        )


class IssueExamplesSerializer(serializers.Serializer):
    reader_id = serializers.IntegerField(label=domain.IssuanceDelivery.reader_id.title)
    issuance_date = serializers.DateField(label=domain.IssuanceDelivery.issuance_date.title)
    examples = serializers.ListField(child=serializers.IntegerField())


class IssuanceSerializer(serializers.Serializer):
    reader_id = serializers.IntegerField(label=domain.IssuanceDelivery.reader_id.title)
    book_registry_ids = serializers.ListField(child=serializers.IntegerField())


class AutoIssueExamplesSerializer(serializers.Serializer):
    issuance_date = serializers.DateField(label=domain.IssuanceDelivery.issuance_date.title)
    count = serializers.IntegerField(min_value=1)
    issued = IssuanceSerializer(many=True)


class DeliverExamplesSerializer(serializers.Serializer):
    issued_ids = serializers.ListField(child=serializers.IntegerField())
    fact_delivery_date = serializers.DateField(label=domain.IssuanceDelivery.fact_delivery_date.title)
    special_notes = serializers.CharField(label=domain.IssuanceDelivery.special_notes.title, max_length=300)


class ProlongIssuanceSerializer(serializers.Serializer):
    extension_days_count = serializers.IntegerField(
        min_value=1,
        label=domain.IssuanceDelivery.extension_days_count.title,
    )
