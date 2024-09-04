# pylint: disable=abstract-method
from rest_framework import (
    serializers,
)

from edulib.core.academic_years.domain import (
    AcademicYear,
)
from edulib.core.classyears import (
    domain,
)
from edulib.core.classyears.models import (
    ClassYear,
)
from edulib.core.parallels.domain.model import (
    Parallel,
)
from edulib.core.persons.domain import (
    Person,
)
from edulib.core.schools.domain import (
    School,
)


class ClassYearSchoolSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='school_id', label=School.id.title)
    short_name = serializers.CharField(source='school__short_name', label=School.short_name.title)


class ClassYearAcademicYearSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='academic_year_id', label=AcademicYear.id.title)
    name = serializers.CharField(source='academic_year__name', label=AcademicYear.name.title)


class ClassYearTeacherSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='teacher_id')
    firstname = serializers.CharField(source='teacher__firstname', label=Person.firstname.title)
    surname = serializers.CharField(source='teacher__surname', label=Person.surname.title)
    patronymic = serializers.CharField(source='teacher__patronymic', label=Person.patronymic.title)


class ClassYearParallelSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='parallel_id', label=Parallel.id.title)
    title = serializers.CharField(source='parallel__title', label=Parallel.title.title)


class ClassYearSerializer(serializers.ModelSerializer):
    school = ClassYearSchoolSerializer(source='*', label=domain.ClassYear.school_id.title)
    academic_year = ClassYearAcademicYearSerializer(source='*', label=domain.ClassYear.academic_year_id.title)
    teacher = ClassYearTeacherSerializer(source='*', label=domain.ClassYear.teacher_id.title)
    parallel = ClassYearParallelSerializer(source='*', label=domain.ClassYear.parallel_id.title)

    class Meta:
        model = ClassYear
        fields = (
            'id',
            'school',
            'academic_year',
            'teacher',
            'parallel',
            'name',
        )
