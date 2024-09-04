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

from edulib.core.lib_publishings.domain import (
    services,
)
from edulib.core.lib_publishings.domain.factories import (
    PublishingDTO,
)
from edulib.core.lib_publishings.services.validators import (
    PublishingValidator,
)


if TYPE_CHECKING:
    from edulib.core.lib_publishings.domain.commands import (
        CreatePublishing,
        DeletePublishing,
        UpdatePublishing,
    )
    from edulib.core.lib_publishings.domain.model import (
        Publishing,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

@handle_pydantic_validation_error
def create_publishing(
    command: 'CreatePublishing',
    uow: 'UnitOfWork',
) -> 'Publishing':
    with uow.wrap():
        publishing = PublishingDTO(**asdict(command))

        validator = PublishingValidator(publishing, uow)
        if errors := validator.validate_similar().get_errors():
            raise DomainValidationError(errors)

        return services.create_publishing(publishing, uow)


@handle_pydantic_validation_error
def update_publishing(
    command: 'UpdatePublishing',
    uow: 'UnitOfWork',
) -> 'Publishing':
    with uow.wrap():
        publishing = PublishingDTO(**asdict(command))

        validator = PublishingValidator(publishing, uow)
        if errors := validator.validate_existence().validate_similar().get_errors():
            raise DomainValidationError(errors)

        return services.update_publishing(publishing, uow)

@handle_pydantic_validation_error
def delete_publishing(
    command: 'DeletePublishing',
    uow: 'UnitOfWork',
) -> None:
    with uow.wrap():
        publishing = PublishingDTO(**asdict(command))

        validator = PublishingValidator(publishing, uow)
        if errors := validator.validate_existence().validate_examples().get_errors():
            raise DomainValidationError(errors)

        services.delete_publishing(publishing, uow)
