from typing import (
    Optional,
    Union,
)

from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
)
from explicit.domain import (
    Unset,
    unset,
)
from explicit.messagebus.commands import (
    Command,
)


class CreateDocument(Command):

    library_passport_id: int
    doc_type: Union[int, None, Unset] = unset
    name: Union[str, None, Unset] = unset
    document: Optional[InMemoryUploadedFile]

    class Config:
        title = 'Команда создания документа'
        arbitrary_types_allowed = True


class UpdateDocument(Command):

    id: int
    doc_type: Union[int, None, Unset] = unset
    name: Union[str, None, Unset] = unset
    document: Optional[InMemoryUploadedFile]

    class Config:
        title = 'Команда обновления документа'
        arbitrary_types_allowed = True


class DeleteDocument(Command):

    id: int

    class Config:
        title = 'Команда удаления документа'
