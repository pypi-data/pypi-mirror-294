# pylint: disable=abstract-method
from typing import (
    Any,
    Dict,
    List,
)

from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from edulib.core.lib_passport.cleanup_days.models import (
    CleanupDays,
)
from edulib.core.lib_passport.documents.models import (
    LibPassportDocuments,
)
from edulib.core.lib_passport.models import (
    LibPassport,
    WorkMode,
)


class LibraryChiefSerializer(Serializer):
    id = IntegerField(source='employee_id')
    name = CharField(source='short_name')


class AddressSerializer(Serializer):
    id = IntegerField(source='address_id')
    full_address = CharField()


class PassportReadSerializer(ModelSerializer):
    school_id = IntegerField()
    library_chief = LibraryChiefSerializer(source='*')
    address_id = AddressSerializer(source='*')
    academic_year_id = IntegerField()

    class Meta:
        model = LibPassport
        fields = (
            'id',
            'school_id',
            'name',
            'library_chief',
            'date_found_month',
            'date_found_year',
            'telephone',
            'address_id',
            'academic_year_id',
            'email',
            'is_address_match',
            'is_telephone_match',
            'is_email_match',
        )


class PassportSerializer(ModelSerializer):
    school_id = IntegerField(required=False)
    library_chief_id = IntegerField(required=False)
    address_id = IntegerField(required=False)
    academic_year_id = IntegerField(required=False)

    class Meta:
        model = LibPassport
        fields = (
            'id',
            'school_id',
            'name',
            'library_chief_id',
            'date_found_month',
            'date_found_year',
            'telephone',
            'address_id',
            'academic_year_id',
            'email',
            'is_address_match',
            'is_telephone_match',
            'is_email_match',
        )


class WorkModeSerializer(ModelSerializer):
    lib_passport_id = IntegerField()
    cleanup_days = SerializerMethodField()

    class Meta:
        model = WorkMode
        fields = (
            'id',
            'lib_passport_id',
            'schedule_mon_from',
            'schedule_mon_to',
            'schedule_tue_from',
            'schedule_tue_to',
            'schedule_wed_from',
            'schedule_wed_to',
            'schedule_thu_from',
            'schedule_thu_to',
            'schedule_fri_from',
            'schedule_fri_to',
            'schedule_sat_from',
            'schedule_sat_to',
            'schedule_sun_from',
            'schedule_sun_to',
            'cleanup_days',
        )

    def get_cleanup_days(self, obj) -> List[Dict[str, Any]]:
        cleanup_days = CleanupDays.objects.filter(lib_passport_id=obj.lib_passport_id)
        return CleanupDayInWorkModeSerializer(cleanup_days, many=True).data


class DocumentSerializer(ModelSerializer):
    library_passport_id = IntegerField()

    class Meta:
        model = LibPassportDocuments
        fields = (
            'id',
            'library_passport_id',
            'doc_type',
            'name',
            'document',
        )


class CleanupDaySerializer(ModelSerializer):
    lib_passport_id = IntegerField()

    class Meta:
        model = CleanupDays
        fields = (
            'id',
            'lib_passport_id',
            'cleanup_date',
        )


class CleanupDayInWorkModeSerializer(ModelSerializer):

    class Meta:
        model = CleanupDays
        fields = (
            'id',
            'cleanup_date',
        )
