from typing import (
    TYPE_CHECKING,
)

from explicit.domain.validation.exceptions import (
    DomainValidationError,
)

from edulib.core.lib_authors.domain import (
    services,
)
from edulib.core.lib_authors.domain.factories import (
    AuthorDTO,
)
from edulib.core.lib_authors.services.validators import (
    AuthorValidator,
)


if TYPE_CHECKING:
    from edulib.core.lib_authors.domain.commands import (
        CreateAuthor,
        DeleteAuthor,
        UpdateAuthor,
    )
    from edulib.core.lib_authors.domain.model import (
        Author,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def create_author(
    command: 'CreateAuthor',
    uow: 'UnitOfWork',
) -> 'Author':
    with uow.wrap():
        author = AuthorDTO(**command.dict())

        validator = AuthorValidator(author, uow)
        errors = validator.validate_name().get_errors()

        if errors:
            raise DomainValidationError(errors)

        return services.create_author(author)


def update_author(
    command: 'UpdateAuthor',
    uow: 'UnitOfWork',
) -> 'Author':
    with uow.wrap():
        author = AuthorDTO(**command.dict())

        validator = AuthorValidator(author, uow)
        errors = validator.validate_existence().validate_name().get_errors()

        if errors:
            raise DomainValidationError(errors)

        return services.update_author(author)


def delete_author(
    command: 'DeleteAuthor',
    uow: 'UnitOfWork',
) -> None:
    author = AuthorDTO(**command.dict())

    validator = AuthorValidator(author, uow)
    errors = validator.validate_existence().get_errors()

    if errors:
        raise DomainValidationError(errors)

    services.delete_author(author)
