from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)

from . import (
    domain,
)


class ClassYear(BaseModel):
    """Проекция "Класс"."""

    id = models.CharField(
        primary_key=True,
        verbose_name=domain.ClassYear.id.title,
        max_length=domain.ClassYear.id.max_length,
    )
    school_id = models.BigIntegerField(
        verbose_name=domain.ClassYear.school_id.title,
    )
    name = models.CharField(
        verbose_name=domain.ClassYear.name.title,
        max_length=domain.ClassYear.name.max_length,
    )
    parallel_id = models.BigIntegerField(
        verbose_name=domain.ClassYear.parallel_id.title,
    )
    letter = models.CharField(
        verbose_name=domain.ClassYear.letter.title,
        max_length=domain.ClassYear.letter.max_length,
        null=True, blank=True
    )
    teacher_id = models.BigIntegerField(
        verbose_name=domain.ClassYear.teacher_id.title,
        null=True, blank=True
    )
    academic_year_id = models.BigIntegerField(
        verbose_name=domain.ClassYear.academic_year_id.title
    )
    open_at = models.DateField(
        verbose_name=domain.ClassYear.open_at.title,
        null=True, blank=True
    )
    close_at = models.DateField(
        verbose_name=domain.ClassYear.close_at.title,
        null=True, blank=True
    )

    class Meta:
        db_table = 'class_year'
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'
