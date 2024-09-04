"""Модели федерального перечня учебников."""
from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)


class FederalBooksParallel(BaseModel):
    """Модель связь параллели и учебника федерального перечня."""

    parallel = models.ForeignKey(
        to='parallels.Parallel',
        verbose_name='Параллели',
        on_delete=models.CASCADE,
    )
    federal_book = models.ForeignKey(
        to='FederalBook',
        verbose_name='Учебник федерального перечня',
        on_delete=models.CASCADE,
    )


class FederalBook(BaseModel):
    """Учебник федерального перечня."""

    name = models.CharField(
        'Наименование',
        max_length=500,
        db_index=True
    )

    publishing = models.ForeignKey(
        to='lib_publishings.LibraryPublishings',
        verbose_name='Издательство',
        on_delete=models.CASCADE,
    )
    pub_lang = models.CharField(
        'Язык издания',
        max_length=100,
        blank=True,
        null=True,
    )
    author = models.ForeignKey(
        to='lib_authors.LibraryAuthors',
        verbose_name='Автор(ы)',
        on_delete=models.CASCADE,
    )

    parallel = models.ManyToManyField(
        to='parallels.Parallel',
        verbose_name='Параллели',
        through=FederalBooksParallel,
        )

    status = models.BooleanField(
        'Статус',
        default=True,
    )
    code = models.CharField(
        'Код',
        max_length=50,
        null=True,
        blank=True,
    )

    validity_period = models.DateField(
        'Срок действия',
        null=True,
        blank=True,
    )

    training_manuals = models.CharField(
        'Учебные пособия',
        max_length=1000,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:  # pylint: disable=invalid-str-returned
        """Представление модели."""
        return self.name

    class Meta:
        db_table = 'federal_books'
        ordering = ['name', ]
        verbose_name = 'Учебник федерального перечня'
        verbose_name_plural = 'Учебники федерального перечня'
