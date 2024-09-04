from typing import (
    TYPE_CHECKING,
)

from explicit.domain import (
    DTOBase,
    asdict,
)

from edulib.core.base.validation import (
    Validator,
    may_skip,
)
from edulib.core.lib_publishings.domain import (
    PublishingNotFound,
)
from edulib.core.lib_publishings.domain.factories import (
    PublishingDTO,
    factory,
)
from edulib.core.lib_publishings.domain.model import (
    Publishing,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


class PublishingValidator(Validator):
    def __init__(self, data: DTOBase, uow: 'UnitOfWork') -> None:
        super().__init__(data, uow)

        self._publishing = None

    def validate_existence(self) -> 'PublishingValidator':
        try:
            self._publishing = self._uow.publishings.get_object_by_id(self._data.id)
        except PublishingNotFound as exc:
            self._errors['id'].append(str(exc))
            self._skip_chain = True

        return self

    @may_skip
    def validate_similar(self) -> 'PublishingValidator':
        publishing = self._create_publishing()
        if self._uow.publishings.publishing_exists(publishing):
            self._errors['name'].append('Такое издательство уже существует')

        return self

    @may_skip
    def validate_examples(self) -> 'PublishingValidator':
        if self._uow.publishings.has_examples(self._publishing):
            self._errors['__root__'].append('Невозможно удалить издательство, т.к. имеются экземпляры')

        return self

    def _create_publishing(self) -> Publishing:
        if self._publishing:
            dto = PublishingDTO(**asdict(self._publishing) | self._data.dict())
        else:
            dto = self._data

        return factory.create(dto)
