from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)

from . import (
    domain,
)


class StudyLevel(BaseModel):
    """Проекция "Уровень обучения"."""

    id = models.BigIntegerField(
        primary_key=True,
        verbose_name=domain.StudyLevel.id.title,
    )
    name = models.CharField(
        verbose_name=domain.StudyLevel.name.title,
        max_length=domain.StudyLevel.name.max_length,
        null=True
    )
    short_name = models.CharField(
        verbose_name=domain.StudyLevel.short_name.title,
        max_length=domain.StudyLevel.short_name.max_length,
        null=True
    )
    first_parallel_id = models.BigIntegerField(
        verbose_name=domain.StudyLevel.first_parallel_id.title
    )
    last_parallel_id = models.BigIntegerField(
        verbose_name=domain.StudyLevel.last_parallel_id.title
    )
    object_status = models.BooleanField(
        verbose_name=domain.StudyLevel.object_status.title
    )

    class Meta:
        db_table = 'study_level'
        verbose_name = 'Уровень обучения'
        verbose_name_plural = 'Уровни обучения'
