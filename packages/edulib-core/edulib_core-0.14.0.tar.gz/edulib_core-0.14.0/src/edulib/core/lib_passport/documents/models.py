from django.db import (
    models,
)

from edulib.core.base.files import (
    upload_file_handler,
)
from edulib.core.base.models import (
    BaseModel,
)
from edulib.core.lib_passport.documents.domain.model import (
    DocumentType,
)


class LibPassportDocuments(BaseModel):
    """Документы библиотеки."""
    doc_type = models.PositiveIntegerField(
        verbose_name='Тип документа',
        choices=DocumentType.choices(),
        null=True,
        blank=True
    )
    name = models.CharField(max_length=200, verbose_name='Наименование')
    document = models.FileField(
        upload_to=upload_file_handler,
        max_length=255,
        verbose_name='Файл',
        blank=True,
        null=True
    )

    library_passport = models.ForeignKey(
        verbose_name='Идентификатор паспорта библиотеки',
        to='lib_passport.LibPassport',
        on_delete=models.CASCADE,
        related_name='documents',
    )

    class Meta:
        db_table = 'library_passport_documents'
        verbose_name = 'Документы библиотеки'
        verbose_name_plural = 'Документы библиотеки'
