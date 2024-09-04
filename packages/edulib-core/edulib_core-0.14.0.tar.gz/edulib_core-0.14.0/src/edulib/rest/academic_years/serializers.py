from rest_framework.serializers import (
    ModelSerializer,
)

from edulib.core.academic_years.models import (
    AcademicYear,
)


class AcademicYearSerializer(ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = ('id', 'code', 'date_begin', 'date_end', 'name')
