from typing import (
    Optional,
)

from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
)
from explicit.domain import (
    asdict,
)

from edulib.core.base.validation import (
    Validator,
    may_skip,
)
from edulib.core.lib_passport.documents.domain import (
    Document,
    DocumentDTO,
    DocumentNotFound,
    factory,
)
from edulib.core.lib_passport.documents.helpers import (
    check_max_filesize,
)
from edulib.core.lib_passport.domain import (
    PassportNotFound,
)


class DocumentValidator(Validator):
    """Валидатор документа библиотеки."""

    def __init__(self, data, uow):
        super().__init__(data, uow)
        self._document = None

    def validate_existence(self) -> 'DocumentValidator':
        self._document = self._get_document(self._data.id, 'id')
        if not self._document:
            self._skip_chain = True

        return self

    @may_skip
    def validate_name(self) -> 'DocumentValidator':
        if 'name' in self._data.dict():
            name = self._data.name.strip()
            if name:
                if self._document:
                    dto = DocumentDTO(**asdict(self._document) | self._data.dict())
                else:
                    dto = self._data

                if self._uow.documents.is_exists(factory.create(dto)):
                    self._errors['name'].append('Документ уже существует')

        return self

    @may_skip
    def validate_library_passport(self) -> 'DocumentValidator':
        if 'library_passport_id' in self._data.dict() and self._data.library_passport_id is not None:
            try:
                self._uow.passports.get_object_by_id(self._data.library_passport_id)
            except PassportNotFound as exc:
                self._errors['library_passport_id'].append(str(exc))

        return self

    @may_skip
    def validate_file_size(self) -> 'DocumentValidator':
        if isinstance(self._data.document, InMemoryUploadedFile):
            file_size = self._data.document.size
            try:
                check_max_filesize(file_size)
            except ValueError as e:
                self._errors['file_size'].append(str(e))

        return self

    def _get_document(self, identifier: int, error_name: str) -> Optional[Document]:
        try:
            return self._uow.documents.get_object_by_id(identifier)
        except DocumentNotFound as exc:
            self._errors[error_name].append(str(exc))
