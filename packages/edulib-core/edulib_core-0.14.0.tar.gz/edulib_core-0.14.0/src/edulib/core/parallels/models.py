from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)

from . import (
    domain,
)


class Parallel(BaseModel):
    """Проекция "Параллель"."""

    id = models.BigIntegerField(
        primary_key=True,
        verbose_name=domain.Parallel.id.title,
    )
    title = models.CharField(
        verbose_name=domain.Parallel.title.title,
        max_length=domain.Parallel.title.max_length,
    )
    system_object_id = models.IntegerField(
        verbose_name=domain.Parallel.system_object_id.title
    )
    object_status = models.BooleanField(
        verbose_name=domain.Parallel.object_status.title
    )

    class Meta:
        db_table = 'parallel'
        verbose_name = 'Параллель'
        verbose_name_plural = 'Параллели'
