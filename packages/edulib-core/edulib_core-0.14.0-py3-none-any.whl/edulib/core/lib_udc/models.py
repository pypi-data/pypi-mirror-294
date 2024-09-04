# pylint: disable=invalid-str-returned, import-outside-toplevel
import mptt
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
)
from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)
from edulib.core.lib_udc import (
    domain,
)


class LibraryUDC(BaseModel):
    """Раздел УДК."""

    code = models.CharField(
        verbose_name=domain.Udc.code.title,
        max_length=domain.Udc.code.max_length,
        db_index=True,
    )
    name = models.CharField(
        verbose_name=domain.Udc.name.title,
        max_length=domain.Udc.name.max_length,
        db_index=True,
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def display(self):
        return self.code
    display.json_encode = True

    def __str__(self):
        """Юникодное представление модели."""
        return self.code

    def safe_delete(self):
        # TODO: Циклический импорт.
        # TODO: Выделить метод .get_by_udc(udc) в репозитории
        # TODO: Перенести бизнес-логику из модели в обработчик сервисного слоя
        from edulib.core.lib_registry.models import (
            LibRegistryEntry,
        )
        if LibRegistryEntry.objects.filter(udc=self).exists():
            raise DjangoValidationError(
                'Невозможно удалить раздел УДК, так как в библиотечном реестре '
                'имеются карточки экземпляров этого раздела!')
        self.delete()
        return True

    class Meta:
        db_table = 'lib_udc'
        verbose_name = 'Раздел УДК'
        verbose_name_plural = 'Разделы УДК'


mptt.register(LibraryUDC, order_insertion_by=['code'])
