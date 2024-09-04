from rest_framework.serializers import (
    ModelSerializer,
)

from edulib.core.parallels.models import (
    Parallel,
)


class ParallelSerializer(ModelSerializer):

    class Meta:
        model = Parallel
        fields = ('id', 'title', 'object_status')
