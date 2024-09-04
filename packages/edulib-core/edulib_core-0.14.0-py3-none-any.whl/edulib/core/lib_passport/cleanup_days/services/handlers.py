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

from edulib.core.lib_passport.cleanup_days import (
    domain,
)
from edulib.core.lib_passport.cleanup_days.services.validators import (
    CleanupDayValidator,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


@handle_pydantic_validation_error
def create_cleanup_day(
    command: domain.CreateCleanupDay,
    uow: 'UnitOfWork',
) -> domain.CleanupDay:
    with uow.wrap():
        cleanup_day = domain.CleanupDayDTO(**asdict(command))

        validator = CleanupDayValidator(cleanup_day, uow)
        errors = (
            validator
            .validate_cleanup_date()
            .get_errors())
        if errors:
            raise DomainValidationError(errors)

        return domain.create_cleanup_day(cleanup_day, uow)


@handle_pydantic_validation_error
def delete_cleanup_day(
    command: domain.DeleteCleanupDay,
    uow: 'UnitOfWork',
) -> None:
    with uow.wrap():
        cleanup_day = domain.CleanupDayDTO(**asdict(command))

        validator = CleanupDayValidator(cleanup_day, uow)
        errors = validator.validate_existence().get_errors()
        if errors:
            raise DomainValidationError(errors)

        domain.delete_cleanup_day(cleanup_day, uow)
