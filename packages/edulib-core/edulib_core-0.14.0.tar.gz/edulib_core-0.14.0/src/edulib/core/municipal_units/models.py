from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)

from . import (
    domain,
)


class MunicipalUnit(BaseModel):
    """Проекция "Муниципальная единица"."""

    id = models.BigIntegerField(
        primary_key=True,
        verbose_name=domain.MunicipalUnit.id.title,
    )
    name = models.TextField(
        verbose_name=domain.MunicipalUnit.name.title,
        null=True
    )
    constituent_entity = models.CharField(
        verbose_name=domain.MunicipalUnit.constituent_entity.title,
        max_length=domain.MunicipalUnit.constituent_entity.max_length,
    )
    oktmo = models.CharField(
        verbose_name=domain.MunicipalUnit.oktmo.title,
        max_length=domain.MunicipalUnit.oktmo.max_length,
        null=True

    )

    class Meta:
        db_table = 'municipal_unit'
        verbose_name = 'Муниципальная единица'
        verbose_name_plural = 'Муниципальные единицы'
