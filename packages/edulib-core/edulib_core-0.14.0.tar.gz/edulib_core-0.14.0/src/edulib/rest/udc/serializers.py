from rest_framework.fields import (
    IntegerField,
)
from rest_framework.serializers import (
    ModelSerializer,
)

from edulib.core.lib_udc.models import (
    LibraryUDC,
)


class UdcSerializer(ModelSerializer):

    parent_id = IntegerField(
        label='Идентификатор родительского раздела',
        required=False,
        allow_null=True,
        min_value=1,
    )

    class Meta:
        model = LibraryUDC
        fields = ('id', 'code', 'name', 'parent_id')
