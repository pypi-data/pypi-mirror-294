from rest_framework import (
    serializers,
)
from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
)

from edulib.core.directory.models import (
    Catalog,
)


class BbkSerializer(ModelSerializer):

    parent_id = IntegerField(
        label='Идентификатор родительского раздела',
        required=False,
        allow_null=True,
        min_value=1,
    )

    class Meta:
        model = Catalog
        fields = ('id', 'code', 'name', 'parent_id')


class BbkDisplaySerializer(BbkSerializer):

    is_leaf = serializers.SerializerMethodField()

    class Meta(BbkSerializer.Meta):
        fields = (
            *BbkSerializer.Meta.fields,
            'is_leaf'
        )

    def get_is_leaf(self, obj: Catalog) -> bool:
        """
        Определяет, является ли узел модели Catalog листовым.

        Проверяет, имеет ли узел дочерние элементы, используя метод
        `is_leaf_node` из django-mptt.

        Args:
            obj: Экземпляр модели Catalog, для которого необходимо определить,
                 является ли он листовым узлом.

        Returns:
            bool: True, если узел является листовым (не имеет потомков), иначе False.
        """
        return obj.is_leaf_node()
