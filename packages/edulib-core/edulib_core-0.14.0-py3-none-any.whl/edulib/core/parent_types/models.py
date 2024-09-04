from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)

from . import (
    domain,
)


class ParentType(BaseModel):
    """Проекция "Тип представителя"."""

    id = models.BigIntegerField(
        primary_key=True,
        verbose_name=domain.ParentType.id.title,
    )
    code = models.CharField(
        verbose_name=domain.ParentType.code.title,
        max_length=domain.ParentType.code.max_length,
        null=True
    )
    name = models.CharField(
        verbose_name=domain.ParentType.name.title,
        max_length=domain.ParentType.name.max_length,
    )
    status = models.BooleanField(
        verbose_name=domain.ParentType.status.title
    )

    class Meta:
        db_table = 'parent_type'
        verbose_name = 'Тип представителя'
        verbose_name_plural = 'Типы представителей'
