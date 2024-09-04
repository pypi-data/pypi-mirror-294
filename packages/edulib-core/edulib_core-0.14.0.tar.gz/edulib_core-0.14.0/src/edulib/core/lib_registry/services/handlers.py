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

from edulib.core.lib_registry import (
    domain,
)
from edulib.core.lib_registry.services.validators import (
    RegistryEntryValidator,
    RegistryExampleValidator,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


@handle_pydantic_validation_error
def create_registry_entry(
    command: domain.CreateRegistryEntry,
    uow: 'UnitOfWork',
) -> domain.RegistryEntry:
    with uow.wrap():
        registry_entry = domain.RegistryEntryDTO(**asdict(command))

        validator = RegistryEntryValidator(registry_entry, uow)
        errors = validator.validate().get_errors()
        if errors:
            raise DomainValidationError(errors)

        return domain.create_registry_entry(registry_entry, uow)


@handle_pydantic_validation_error
def update_registry_entry(
    command: domain.UpdateRegistryEntry,
    uow: 'UnitOfWork',
) -> domain.RegistryEntry:
    with uow.wrap():
        registry_entry = domain.RegistryEntryDTO(**asdict(command))

        validator = RegistryEntryValidator(registry_entry, uow)
        errors = validator.validate_existence().validate().get_errors()
        if errors:
            raise DomainValidationError(errors)

        return domain.update_registry_entry(registry_entry, uow)


@handle_pydantic_validation_error
def delete_registry_entry(
    command: domain.DeleteRegistryEntry,
    uow: 'UnitOfWork',
) -> None:
    with uow.wrap():
        registry_entry = domain.RegistryEntryDTO(**asdict(command))

        validator = RegistryEntryValidator(registry_entry, uow)
        errors = validator.validate_existence().validate_examples().get_errors()
        if errors:
            raise DomainValidationError(errors)

        domain.delete_registry_entry(registry_entry, uow)


@handle_pydantic_validation_error
def create_registry_example(
    command: domain.CreateRegistryExample,
    uow: 'UnitOfWork',
) -> domain.RegistryExample:
    with uow.wrap():
        registry_example = domain.RegistryExampleDTO(**asdict(command))

        validator = RegistryExampleValidator(registry_example, uow)
        if errors := validator.validate_entry().validate_publishing().get_errors():
            raise DomainValidationError(errors)

        return domain.create_registry_example(registry_example, uow)


@handle_pydantic_validation_error
def update_registry_example(
    command: domain.UpdateRegistryExample,
    uow: 'UnitOfWork',
) -> domain.RegistryExample:
    with uow.wrap():
        registry_example = domain.RegistryExampleDTO(**asdict(command))

        validator = RegistryExampleValidator(registry_example, uow)
        if errors := validator.validate_existence().validate_publishing().get_errors():
            raise DomainValidationError(errors)

        return domain.update_registry_example(registry_example, uow)


@handle_pydantic_validation_error
def delete_registry_example(
    command: domain.DeleteRegistryExample,
    uow: 'UnitOfWork',
) -> None:
    with uow.wrap():
        registry_example = domain.RegistryExampleDTO(**asdict(command))

        validator = RegistryExampleValidator(registry_example, uow)
        if errors := validator.validate_existence().get_errors():
            raise DomainValidationError(errors)

        domain.delete_registry_example(registry_example, uow)


@handle_pydantic_validation_error
def copy_registry_example(
    command: domain.CopyRegistryExample,
    uow: 'UnitOfWork',
) -> None:
    with uow.wrap():
        registry_example = domain.RegistryExampleDTO(**asdict(command))

        validator = RegistryExampleValidator(registry_example, uow)
        if errors := validator.validate_existence().get_errors():
            raise DomainValidationError(errors)

        domain.copy_registry_example(registry_example, uow)
