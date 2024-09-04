from collections import (
    OrderedDict,
)
from typing import (
    Union,
)

from rest_framework import (
    serializers,
)

from edulib.core.directory.models import (
    Catalog,
)
from edulib.core.federal_books.models import (
    FederalBook,
)
from edulib.core.lib_authors.models import (
    LibraryAuthors,
)
from edulib.core.lib_example_types.models import (
    LibraryExampleType,
)
from edulib.core.lib_registry import (
    domain,
)
from edulib.core.lib_registry.models import (
    LibMarkInformProduct,
    LibRegistryEntry,
)
from edulib.core.lib_sources.models import (
    LibrarySource,
)
from edulib.core.lib_udc.models import (
    LibraryUDC,
)
from edulib.core.parallels.models import (
    Parallel,
)


class IdNameSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
        )


class LibMarkInformProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibMarkInformProduct
        fields = (
            'id',
            'code',
        )


class LibraryExampleTypeSerializer(IdNameSerializer):
    class Meta(IdNameSerializer.Meta):
        model = LibraryExampleType


class ShortAuthorSerializer(IdNameSerializer):
    class Meta(IdNameSerializer.Meta):
        model = LibraryAuthors


class ParallelShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parallel
        fields = (
            'id',
            'title',
        )


class BbcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = (
            'id',
            'name',
            'code',
        )


class ShortUdcSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryUDC
        fields = (
            'id',
            'name',
            'code',
        )


class ShortFederalBookSerializer(IdNameSerializer):
    class Meta(IdNameSerializer.Meta):
        model = FederalBook


class BaseEntrySerializer(serializers.ModelSerializer):
    author = ShortAuthorSerializer(label=domain.RegistryEntry.author_id.title)
    type = LibraryExampleTypeSerializer(label=domain.RegistryEntry.type_id.title)
    parallels = ParallelShortSerializer(many=True, label=domain.RegistryEntry.parallel_ids.title)
    age_tag = LibMarkInformProductSerializer(label=domain.RegistryEntry.age_tag_id.title)
    editions = serializers.CharField()
    publishings = serializers.CharField()
    publishing_years = serializers.CharField()
    discipline = serializers.SerializerMethodField(label=domain.RegistryEntry.discipline_id.title)
    bbc = BbcSerializer(label=domain.RegistryEntry.bbc_id.title)
    udc = ShortUdcSerializer(label=domain.RegistryEntry.udc_id.title)
    count = serializers.IntegerField()
    free_count = serializers.IntegerField()
    federal_book = ShortFederalBookSerializer(label=domain.RegistryEntry.federal_book_id.title)

    class Meta:
        model = LibRegistryEntry
        fields = (
            'id',
            'title',
            'author',
            'type',
            'discipline',
            'parallels',
            'editions',
            'age_tag',
            'publishings',
            'status',
            'publishing_years',
            'bbc',
            'udc',
            'count',
            'free_count',
            'federal_book',
        )

    def to_representation(self, instance: LibRegistryEntry) -> OrderedDict:
        instance.status = instance.get_status_display()

        return super().to_representation(instance)

    def get_discipline(self, obj: LibRegistryEntry) -> dict[str, Union[str, int]]:
        return {
            'id': obj.discipline_id,
            'name': obj.discipline_name,
        }


class EntryListSerializer(BaseEntrySerializer):
    class Meta(BaseEntrySerializer.Meta):
        pass


class LibrarySourceSerializer(IdNameSerializer):
    class Meta(IdNameSerializer.Meta):
        model = LibrarySource


class EntryRetrieveSerializer(BaseEntrySerializer):
    source = LibrarySourceSerializer()

    class Meta(BaseEntrySerializer.Meta):
        fields = (
            *BaseEntrySerializer.Meta.fields,
            'source',
            'short_info',
            'filename',
            'cover',
        )


class EntrySerializer(serializers.ModelSerializer):
    type_id = serializers.IntegerField(label=domain.RegistryEntry.type_id.title)
    title = serializers.CharField(
        label=domain.RegistryEntry.title.title,
        max_length=domain.RegistryEntry.title.max_length,
        required=False,
    )
    author_id = serializers.IntegerField(label=domain.RegistryEntry.author_id.title, required=False)
    parallel_ids = serializers.ListField(
        label=domain.RegistryEntry.parallel_ids.title,
        child=serializers.IntegerField(),
        required=False,
    )
    udc_id = serializers.IntegerField(label=domain.RegistryEntry.udc_id.title, required=False, allow_null=True)
    bbc_id = serializers.IntegerField(label=domain.RegistryEntry.bbc_id.title, required=False, allow_null=True)
    source_id = serializers.IntegerField(label=domain.RegistryEntry.source_id.title, required=False, allow_null=True)
    age_tag_id = serializers.IntegerField(label=domain.RegistryEntry.age_tag_id.title, required=False, allow_null=True)
    federal_book_id = serializers.IntegerField(
        label=domain.RegistryEntry.federal_book_id.title,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = LibRegistryEntry
        fields = (
            'id',
            'type_id',
            'title',
            'author_id',
            'parallel_ids',
            'author_sign',
            'udc_id',
            'bbc_id',
            'tags',
            'source_id',
            'short_info',
            'on_balance',
            'school_id',
            'filename',
            'cover',
            'discipline_id',
            'age_tag_id',
            'status',
            'federal_book_id',
        )


class GeneralFundSerializer(BaseEntrySerializer):
    municipal_unit = serializers.SerializerMethodField()
    school = serializers.SerializerMethodField()
    lack = serializers.IntegerField(read_only=True)
    excess = serializers.IntegerField(read_only=True)
    sufficiency = serializers.IntegerField(read_only=True)

    def get_school(self, obj: LibRegistryEntry) -> dict[str, Union[str, int]]:
        return {
            'id': obj.school_id,
            'name': obj.school_name,
        }

    def get_municipal_unit(self, obj: LibRegistryEntry) -> dict[str, Union[str, int]]:
        return {
            'id': obj.municipal_unit_id,
            'name': obj.municipal_unit_name,
        }

    class Meta(BaseEntrySerializer.Meta):
        model = LibRegistryEntry
        fields = (
            *BaseEntrySerializer.Meta.fields,
            'municipal_unit',
            'school',
            'lack',
            'excess',
            'sufficiency',
        )
