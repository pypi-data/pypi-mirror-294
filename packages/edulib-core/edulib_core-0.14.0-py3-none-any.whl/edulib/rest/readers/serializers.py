# pylint: disable=abstract-method
from collections import (
    OrderedDict,
)
from typing import (
    Any,
)

from rest_framework import (
    serializers,
)

from edulib.core.readers import (
    domain,
)
from edulib.core.readers.models import (
    Reader,
)


class SchoolShortSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='dependent_school_id')
    shortname = serializers.CharField(source='school_shortname')


class ClassYearSerializer(serializers.Serializer):
    id = serializers.CharField(source='class_year_id')
    name = serializers.CharField(source='class_year_name')


class PersonSerializer(serializers.Serializer):
    id = serializers.CharField(source='person_id')
    firstname = serializers.CharField()
    surname = serializers.CharField()
    patronymic = serializers.CharField()


class EmployeeSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='teacher_id')
    person = PersonSerializer(source='*')
    class_year = ClassYearSerializer(source='*')
    school = SchoolShortSerializer(source='*')


class SchoolchildSerializer(serializers.Serializer):
    person = PersonSerializer(source='*')
    class_year = ClassYearSerializer(source='*')
    school = SchoolShortSerializer(source='*')


class ReaderSerializer(serializers.ModelSerializer):
    overdue_examples_count = serializers.IntegerField()
    employee = serializers.SerializerMethodField()
    pupil = serializers.SerializerMethodField()

    class Meta:
        model = Reader
        fields = (
            'id',
            'number',
            'role',
            'overdue_examples_count',
            'employee',
            'pupil',
        )

    def get_employee(self, obj: Reader) -> OrderedDict[str, Any]:
        if obj.teacher_id:
            serializer = EmployeeSerializer(obj)

            return serializer.data

    def get_pupil(self, obj: Reader) -> OrderedDict[str, Any]:
        if obj.schoolchild_id:
            serializer = SchoolchildSerializer(obj)

            return serializer.data

    def to_representation(self, instance: Reader) -> OrderedDict[str, Any]:
        instance.role = instance.get_role_display()

        return super().to_representation(instance)


class ReaderUpdateSerializer(serializers.Serializer):
    number = serializers.CharField(label=domain.Reader.number.title)
