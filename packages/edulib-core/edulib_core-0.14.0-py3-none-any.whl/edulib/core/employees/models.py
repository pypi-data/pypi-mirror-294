from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)

from . import (
    domain,
)


class Employee(BaseModel):
    """Проекция "Сотрудник"."""

    id = models.BigIntegerField(
        primary_key=True,
        verbose_name=domain.Employee.id.title,
    )
    person = models.ForeignKey(
        to='persons.Person',
        verbose_name=domain.Employee.person_id.title,
        on_delete=models.CASCADE
    )
    school_id = models.BigIntegerField(
        verbose_name=domain.Employee.school_id.title,
    )
    info_date_begin = models.DateField(
        verbose_name=domain.Employee.info_date_begin.title
    )
    info_date_end = models.DateField(
        verbose_name=domain.Employee.info_date_end.title,
        null=True
    )
    personnel_num = models.CharField(
        verbose_name=domain.Employee.personnel_num.title,
        max_length=domain.Employee.personnel_num.max_length,
        null=True
    )
    job_code = models.BigIntegerField(
        verbose_name=domain.Employee.job_code.title,
        null=True
    )
    job_name = models.CharField(
        verbose_name=domain.Employee.job_name.title,
        max_length=domain.Employee.job_name.max_length,
        null=True
    )
    employment_kind_id = models.BigIntegerField(
        verbose_name=domain.Employee.employment_kind_id.title,
    )
    object_status = models.BooleanField(
        verbose_name=domain.Employee.object_status.title
    )

    class Meta:
        db_table = 'employee'
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
