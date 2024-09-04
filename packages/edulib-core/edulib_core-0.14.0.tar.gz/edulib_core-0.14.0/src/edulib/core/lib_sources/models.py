# pylint: disable=invalid-str-returned
from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)


class LibrarySource(BaseModel):

    """Источник поступления книг в библиотеку"""

    name = models.TextField(
        verbose_name='Источник поступления',
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'library_source'
        ordering = ('name',)
        verbose_name = 'Источник поступления'
        verbose_name_plural = 'Источники поступления'
