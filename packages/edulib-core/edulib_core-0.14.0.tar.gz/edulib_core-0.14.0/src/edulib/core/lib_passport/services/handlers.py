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

from edulib.core.lib_passport import (
    domain,
)
from edulib.core.lib_passport.services.validators import (
    PassportValidator,
    WorkModeValidator,
)


if TYPE_CHECKING:
    from edulib.core.schools import (
        domain as schools,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


@handle_pydantic_validation_error
def create_passport(
    command: domain.CreatePassport,
    uow: 'UnitOfWork',
) -> domain.Passport:
    with uow.wrap():
        passport = domain.PassportDTO(**asdict(command))

        validator = PassportValidator(passport, uow)
        errors = (
            validator
            .validate_name()
            .validate_school()
            .validate_address()
            .validate_academic_year()
            .validate_library_chief()
            .get_errors())
        if errors:
            raise DomainValidationError(errors)

        return domain.create_passport(passport, uow)


@handle_pydantic_validation_error
def update_passport(
    command: domain.UpdatePassport,
    uow: 'UnitOfWork',
) -> domain.Passport:
    with uow.wrap():
        passport = domain.PassportDTO(**asdict(command))

        validator = PassportValidator(passport, uow)
        errors = (
            validator
            .validate_existence()
            .validate_name(is_update=True)
            .validate_address()
            .validate_academic_year()
            .validate_library_chief()
            .get_errors()
        )
        if errors:
            raise DomainValidationError(errors)

        return domain.update_passport(passport, uow)


@handle_pydantic_validation_error
def delete_passport(
    command: domain.DeletePassport,
    uow: 'UnitOfWork',
) -> None:
    with uow.wrap():
        passport = domain.PassportDTO(**asdict(command))

        validator = PassportValidator(passport, uow)
        errors = validator.validate_existence().get_errors()
        if errors:
            raise DomainValidationError(errors)

        domain.delete_passport(passport, uow)


@handle_pydantic_validation_error
def create_work_mode(
    command: domain.CreateWorkMode,
    uow: 'UnitOfWork',
) -> domain.WorkMode:
    with uow.wrap():
        work_mode = domain.WorkModeDTO(**asdict(command))
        validator = WorkModeValidator(work_mode, uow)
        errors = validator.validate_lib_passport().get_errors()
        if errors:
            raise DomainValidationError(errors)

        return domain.create_work_mode(work_mode, uow)


@handle_pydantic_validation_error
def update_work_mode(
    command: domain.UpdateWorkMode,
    uow: 'UnitOfWork',
) -> domain.WorkMode:
    with uow.wrap():
        work_mode = domain.WorkModeDTO(**asdict(command))

        validator = WorkModeValidator(work_mode, uow)
        errors = validator.validate_existence().validate_lib_passport().get_errors()
        if errors:
            raise DomainValidationError(errors)

        return domain.update_work_mode(work_mode, uow)


@handle_pydantic_validation_error
def delete_work_mode(
    command: domain.DeleteWorkMode,
    uow: 'UnitOfWork',
) -> None:
    with uow.wrap():
        work_mode = domain.WorkModeDTO(**asdict(command))

        validator = WorkModeValidator(work_mode, uow)
        errors = validator.validate_existence().get_errors()
        if errors:
            raise DomainValidationError(errors)

        domain.delete_work_mode(work_mode, uow)


def on_school_projection_created(
    event: 'schools.SchoolProjectionCreated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.create_default_passport_for_school(event.school, uow)


def on_school_projection_updated(
    event: 'schools.SchoolProjectionUpdated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.create_default_passport_for_school(event.school, uow)
