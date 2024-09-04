# pylint: disable=abstract-method
from rest_framework import (
    serializers,
)
from rest_framework.serializers import (
    ModelSerializer,
)

from edulib.core.schools.models import (
    School,
)


class FAddressShortSerializer(serializers.Serializer):
    id = serializers.CharField(source='f_address_id')
    full_address = serializers.CharField(source='f_address_name')


class UAddressShortSerializer(serializers.Serializer):
    id = serializers.CharField(source='u_address_id')
    full_address = serializers.CharField(source='u_address_name')


class InstitutionTypeShortSerializer(serializers.Serializer):
    id = serializers.CharField(source='institution_type_id')
    name = serializers.CharField(source='institution_type_name')


class SchoolSerializer(ModelSerializer):
    f_addr = FAddressShortSerializer(source='*')
    u_addr = UAddressShortSerializer(source='*')
    institution_type = InstitutionTypeShortSerializer(source='*')

    class Meta:
        model = School
        fields = (
            'id',
            'short_name',
            'name',
            'kpp',
            'okato',
            'oktmo',
            'okpo',
            'ogrn',
            'inn',
            'telephone',
            'email',
            'website',
            'fax',
            'manager',
            'institution_type',
            'parent_id',
            'f_addr',
            'u_addr',
        )
