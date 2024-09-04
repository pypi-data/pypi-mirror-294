from explicit.domain import (
    DTOBase,
)

from edulib.core.base.validation import (
    Validator,
)
from edulib.core.readers.domain import (
    ReaderNotFound,
)
from edulib.core.unit_of_work import (
    UnitOfWork,
)


class ReaderValidator(Validator):
    def __init__(self, data: DTOBase, uow: UnitOfWork) -> None:
        super().__init__(data, uow)

        self._reader = None

    def validate_existence(self) -> 'ReaderValidator':
        try:
            self._reader = self._uow.readers.get_object_by_id(self._data.id)
        except ReaderNotFound as exc:
            self._errors['id'].append(str(exc))
            self._skip_chain = True

        return self
