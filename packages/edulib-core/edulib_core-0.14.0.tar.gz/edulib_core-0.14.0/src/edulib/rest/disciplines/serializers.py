from rest_framework.serializers import (
    ModelSerializer,
)

from edulib.core.disciplines.models import (
    Discipline,
)


class DisciplineSerializer(ModelSerializer):
    class Meta:
        model = Discipline
        fields = (
            'id',
            'name',
            'description',
        )
