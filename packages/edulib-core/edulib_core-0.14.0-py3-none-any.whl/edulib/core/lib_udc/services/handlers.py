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

from edulib.core.lib_udc import (
    domain,
)
from edulib.core.lib_udc.services.validators import (
    UdcValidator,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


@handle_pydantic_validation_error
def create_udc(
    command: domain.CreateUdc,
    uow: 'UnitOfWork',
) -> domain.Udc:
    with uow.wrap():
        udc = domain.UdcDTO(**asdict(command))

        validator = UdcValidator(udc, uow)
        errors = validator.validate_parent().validate_code().get_errors()
        if errors:
            raise DomainValidationError(errors)

        return domain.create_udc(udc, uow)


@handle_pydantic_validation_error
def update_udc(
    command: domain.UpdateUdc,
    uow: 'UnitOfWork',
) -> domain.Udc:
    with uow.wrap():
        udc = domain.UdcDTO(**asdict(command))

        validator = UdcValidator(udc, uow)
        errors = validator.validate_existence().validate_parent().validate_code(is_update=True).get_errors()
        if errors:
            raise DomainValidationError(errors)

        return domain.update_udc(udc, uow)


@handle_pydantic_validation_error
def delete_udc(
    command: domain.DeleteUdc,
    uow: 'UnitOfWork',
) -> None:
    with uow.wrap():
        udc = domain.UdcDTO(**asdict(command))

        validator = UdcValidator(udc, uow)
        errors = validator.validate_existence().get_errors()
        if errors:
            raise DomainValidationError(errors)

        domain.delete_udc(udc, uow)
