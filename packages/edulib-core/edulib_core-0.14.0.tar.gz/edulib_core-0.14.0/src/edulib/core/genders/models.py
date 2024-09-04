from django.db import (
    models,
)

from edulib.core.base.models import (
    SimpleDictionary,
)
from edulib.core.genders import (
    domain,
)


class Gender(SimpleDictionary):
    """Проекция "Пол"."""

    id = models.BigIntegerField(
        primary_key=True,
        verbose_name=domain.Gender.id.title,
    )

    class Meta:
        db_table = 'gender'
        verbose_name = 'Пол'
        verbose_name_plural = 'Полы'
