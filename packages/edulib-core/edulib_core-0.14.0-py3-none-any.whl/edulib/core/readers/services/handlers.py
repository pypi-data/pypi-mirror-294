from typing import (
    TYPE_CHECKING,
)

from explicit.domain import (
    asdict,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
    handle_pydantic_validation_error,
)

from edulib.core.readers import (
    domain,
)
from edulib.core.readers.services.validators import (
    ReaderValidator,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


@handle_pydantic_validation_error
def update_reader(
    command: domain.UpdateReader,
    uow: 'UnitOfWork',
) -> domain.Reader:
    with uow.wrap():
        reader = domain.ReaderDTO(**asdict(command))

        validator = ReaderValidator(reader, uow)
        errors = validator.validate_existence().get_errors()
        if errors:
            raise DomainValidationError(errors)

        return domain.update_reader(reader, uow)
