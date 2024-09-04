from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)
from edulib.core.disciplines import (
    domain,
)


class Discipline(BaseModel):
    """Проекция "Предмет"."""

    id = models.BigIntegerField(
        verbose_name=domain.Discipline.id.title,
        primary_key=True,
    )
    name = models.CharField(
        verbose_name=domain.Discipline.name.title,
        max_length=domain.Discipline.name.max_length,
    )
    description = models.TextField(
        verbose_name=domain.Discipline.description.title,
        null=True
    )

    class Meta:
        db_table = 'discipline'
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
