from django.db import (
    models,
)

from edulib.core.base.models import (
    SimpleDictionary,
)
from edulib.core.institution_types import (
    domain,
)


class InstitutionType(SimpleDictionary):
    """Проекция "Тип организации"."""

    id = models.BigIntegerField(
        primary_key=True,
        verbose_name=domain.InstitutionType.id.title,
        max_length=domain.InstitutionType.id.max_length,
    )

    class Meta:
        db_table = 'institution_type'
        verbose_name = 'Тип организации'
        verbose_name_plural = 'Типы организациий'
