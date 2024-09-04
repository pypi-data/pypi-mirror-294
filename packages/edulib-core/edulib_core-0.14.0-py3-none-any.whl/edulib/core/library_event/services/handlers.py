from typing import (
    TYPE_CHECKING,
)

from explicit.domain import (
    asdict,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
)

from edulib.core.library_event import (
    domain,
)
from edulib.core.library_event.services.validators import (
    EventValidator,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def create_event(
    command: domain.CreateEvent,
    uow: 'UnitOfWork',
) -> domain.Event:
    with uow.wrap():
        event = domain.EventDTO(**asdict(command))

        validator = EventValidator(event, uow)
        errors = validator.validate_passport().get_errors()

        if errors:
            raise DomainValidationError(errors)

        return domain.create_event(event, uow)


def update_event(
    command: domain.UpdateEvent,
    uow: 'UnitOfWork',
) -> domain.Event:
    with uow.wrap():
        event = domain.EventDTO(**asdict(command))

        validator = EventValidator(event, uow)
        errors = validator.validate_existence().validate_passport().get_errors()

        if errors:
            raise DomainValidationError(errors)

        return domain.update_event(event, uow)


def delete_event(
    command: domain.DeleteEvent,
    uow: 'UnitOfWork',
) -> None:
    event = domain.EventDTO(**asdict(command))

    validator = EventValidator(event, uow)
    errors = validator.validate_existence().get_errors()

    if errors:
        raise DomainValidationError(errors)

    domain.delete_event(event, uow)
