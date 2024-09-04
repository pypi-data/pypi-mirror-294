from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)


class CleanupDays(BaseModel):
    """Санитарные дни."""

    lib_passport = models.ForeignKey(
        verbose_name='Паспорт библиотеки',
        to='lib_passport.LibPassport',
        on_delete=models.CASCADE,
        related_name='cleanup_days',
        null=True,
        blank=True,
    )
    cleanup_date = models.DateField(verbose_name='Дата санитарного дня')

    class Meta:
        db_table = 'cleanup_days'
        verbose_name = 'Санитарные дни'
        verbose_name_plural = 'Санитарные дни'
