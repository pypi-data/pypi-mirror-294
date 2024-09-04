from typing import (
    TYPE_CHECKING,
)

from explicit.domain.model import (
    asdict,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
    handle_pydantic_validation_error,
)

from edulib.core.federal_books.domain import (
    services,
)
from edulib.core.federal_books.domain.factories import (
    FederalBookDTO,
)
from edulib.core.federal_books.services.validators import (
    FederalBookValidator,
)


if TYPE_CHECKING:
    from edulib.core.federal_books.domain.commands import (
        CreateFederalBook,
        UpdateFederalBook,
    )
    from edulib.core.federal_books.domain.model import (
        FederalBook,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


@handle_pydantic_validation_error
def create_federal_book(
    command: 'CreateFederalBook',
    uow: 'UnitOfWork',
) -> 'FederalBook':
    with uow.wrap():
        federal_book = FederalBookDTO(**asdict(command))

        validator = FederalBookValidator(federal_book, uow)

        errors = validator.validate_parallels().validate_federal_book().get_errors()
        if errors:
            raise DomainValidationError(errors)

        return services.create_federal_book(federal_book, uow)


@handle_pydantic_validation_error
def update_federal_book(
    command: 'UpdateFederalBook',
    uow: 'UnitOfWork',
) -> 'FederalBook':
    with uow.wrap():
        federal_book = FederalBookDTO(**asdict(command))

        validator = FederalBookValidator(federal_book, uow)
        errors = validator.validate_existence().get_errors()
        if errors:
            raise DomainValidationError(errors)

        return services.update_federal_book(federal_book, uow)
