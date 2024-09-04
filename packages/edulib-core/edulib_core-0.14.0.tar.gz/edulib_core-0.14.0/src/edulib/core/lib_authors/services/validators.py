
from typing import (
    TYPE_CHECKING,
)

from explicit.domain.model import (
    asdict,
)

from edulib.core.base.validation import (
    Validator,
    may_skip,
)
from edulib.core.lib_authors.domain import (
    AuthorDTO,
)
from edulib.core.lib_authors.domain.factories import (
    factory,
)
from edulib.core.lib_authors.domain.model import (
    AuthorNotFound,
)


if TYPE_CHECKING:
    from explicit.domain.factories import (
        DTOBase,
    )

    from edulib.core.lib_sources.domain.model import (
        Source,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


class AuthorValidator(Validator):
    """Валидатор авторов."""

    def __init__(self, data: 'DTOBase', uow: 'UnitOfWork') -> None:
        super().__init__(data, uow)

        self._author = None

    def validate_existence(self) -> 'AuthorValidator':
        try:
            self._author = self._uow.authors.get_object_by_id(self._data.id)
        except AuthorNotFound as exc:
            self._errors['id'].append(str(exc))
            self._skip_chain = True

        return self

    @may_skip
    def validate_name(self) -> 'AuthorValidator':
        author = self._create_author()
        if self._uow.authors.author_exists(author):
            self._errors['name'].append('Такой автор уже существует')

        return self


    def _create_author(self) -> 'Source':
        if self._author:
            dto = AuthorDTO(**asdict(self._author) | self._data.dict())
        else:
            dto = self._data

        return factory.create(dto)
