# pylint: disable=abstract-method
from rest_framework import (
    serializers,
)


class GenderSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='person_gender_id')
    name = serializers.CharField(source='person_gender_name')


class PersonSerializer(serializers.Serializer):
    id = serializers.CharField(source='person_id_annotate')
    surname = serializers.CharField(source='person_surname')
    firstname = serializers.CharField(source='person_firstname')
    patronymic = serializers.CharField(source='person_patronymic')
    date_of_birth = serializers.DateField(source='person_date_of_birth')
    gender = GenderSerializer(source='*')


class ClassYearShortSerializer(serializers.Serializer):
    id = serializers.CharField(source='pupil_class_year_id')
    name = serializers.CharField(source='pupil_class_year_name')


class SchoolShortSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='pupil_school_id')
    short_name = serializers.CharField(source='pupil_school_short_name')


class PupilSerializer(serializers.Serializer):
    id = serializers.CharField(source='pupil_id')
    class_year = ClassYearShortSerializer(source='*')
    school = SchoolShortSerializer(source='*')
    training_begin_date = serializers.DateField(source='pupil_training_begin_date')
    training_end_date = serializers.DateField(source='pupil_training_end_date')


class SchoolchildSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    person = PersonSerializer(source='*')
    pupil = PupilSerializer(source='*')
