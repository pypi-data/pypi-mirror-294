"""Модели справочника Издательства."""
from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)


class LibraryPublishings(BaseModel):
    """Справочник Издательства."""

    name = models.CharField('Издательство', max_length=256, db_index=True)

    def __str__(self) -> str:  # pylint: disable=invalid-str-returned
        """Представление модели."""
        return self.name

    class Meta:
        db_table = 'lib_publishings'
        ordering = ['name']
        verbose_name = 'Издательство'
        verbose_name_plural = 'Издательства'
