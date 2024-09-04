from typing import (
    TYPE_CHECKING,
)

from explicit.domain.model import (
    asdict,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
)

from edulib.core.lib_sources.domain import (
    services,
)
from edulib.core.lib_sources.domain.factories import (
    SourceDTO,
)
from edulib.core.lib_sources.services.validators import (
    SourceValidator,
)


if TYPE_CHECKING:
    from edulib.core.lib_sources.domain.commands import (
        CreateSource,
        DeleteSource,
        UpdateSource,
    )
    from edulib.core.lib_sources.domain.model import (
        Source,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def create_source(
    command: 'CreateSource',
    uow: 'UnitOfWork',
) -> 'Source':
    with uow.wrap():
        source = SourceDTO(**asdict(command))

        validator = SourceValidator(source, uow)
        errors = (
            validator
            .validate_name()
            .get_errors()
        )

        if errors:
            raise DomainValidationError(errors)
        return services.create_source(source, uow)


def update_source(
    command: 'UpdateSource',
    uow: 'UnitOfWork',
) -> 'Source':
    with uow.wrap():
        source = SourceDTO(**asdict(command))

        validator = SourceValidator(source, uow)
        errors = (
            validator
            .validate_existence()
            .validate_name()
            .get_errors()
        )

        if errors:
            raise DomainValidationError(errors)

        return services.update_source(source, uow)


def delete_source(
    command: 'DeleteSource',
    uow: 'UnitOfWork',
) -> None:
    source = SourceDTO(**asdict(command))

    validator = SourceValidator(source, uow)
    errors = (
        validator
        .validate_existence()
        .validate_deletion_if_linked_entries_exist()
        .get_errors()
    )

    if errors:
        raise DomainValidationError(errors)

    services.delete_source(source, uow)
