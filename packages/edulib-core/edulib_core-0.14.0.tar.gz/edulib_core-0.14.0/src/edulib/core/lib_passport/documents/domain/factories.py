from typing import (
    Union,
)

from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
)
from explicit.domain import (
    AbstractDomainFactory,
    DTOBase,
    Unset,
    unset,
)

from edulib.core.lib_passport.documents.domain.model import (
    Document,
)


class DocumentDTO(DTOBase):

    id: Union[int, None, Unset] = unset
    library_passport_id: Union[int, None, Unset] = unset
    doc_type: Union[int, None, Unset] = unset
    name: Union[str, None, Unset] = unset
    document: Union[InMemoryUploadedFile, None, Unset] = unset

    class Config:
        arbitrary_types_allowed = True


class Factory(AbstractDomainFactory):

    def create(self, data: DocumentDTO) -> Document:
        return Document(**data.dict())


factory = Factory()
