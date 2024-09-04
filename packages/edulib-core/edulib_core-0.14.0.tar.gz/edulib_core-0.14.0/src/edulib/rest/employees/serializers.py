# pylint: disable=abstract-method
from rest_framework import (
    serializers,
)

from edulib.core.address.domain import (
    Address,
)
from edulib.core.employees import (
    domain,
)
from edulib.core.employees.models import (
    Employee,
)
from edulib.core.genders.domain.model import (
    Gender,
)
from edulib.core.persons.domain import (
    Person,
)
from edulib.core.schools.domain.model import (
    School,
)


class EmployeeSchoolSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='school_id', label=School.id.title)
    short_name = serializers.CharField(source='school__short_name', label=School.short_name.title)


class EmployeeGenderSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='person.gender_id', label=Gender.id.title)
    name = serializers.CharField(source='gender__name', label=Gender.name.title)


class EmployeeAddressSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='person.temp_reg_addr_id', label=Address.id.title)
    full_address = serializers.CharField(source='person__full_address', label=Address.full.title)


class EmployeeSerializer(serializers.ModelSerializer):
    surname = serializers.CharField(source='person.surname', label=Person.surname.title)
    firstname = serializers.CharField(source='person.firstname', label=Person.firstname.title)
    patronymic = serializers.CharField(source='person.patronymic', label=Person.patronymic.title)
    date_of_birth = serializers.CharField(source='person.date_of_birth', label=Person.date_of_birth.title)
    inn = serializers.CharField(source='person.inn', label=Person.inn.title)
    telephone = serializers.CharField(source='person.phone', label=Person.phone.title)
    email = serializers.CharField(source='person.email', label=Person.email.title)
    snils = serializers.CharField(source='person.snils', label=Person.snils.title)
    school = EmployeeSchoolSerializer(source='*', label=domain.Employee.school_id.title)
    gender = EmployeeGenderSerializer(source='*', label=Person.gender_id.title)
    temp_reg_addr = EmployeeAddressSerializer(source='*', label=Person.temp_reg_addr_id.title)
    job_names = serializers.ListField(child=serializers.CharField(), label=domain.Employee.job_name.title)

    class Meta:
        model = Employee
        fields = (
            'id',
            'surname',
            'firstname',
            'patronymic',
            'date_of_birth',
            'school',
            'job_names',
            'gender',
            'inn',
            'telephone',
            'email',
            'snils',
            'temp_reg_addr',
            'person_id',
        )
