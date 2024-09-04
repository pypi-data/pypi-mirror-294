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

from edulib.core.lib_passport.documents import (
    domain,
)
from edulib.core.lib_passport.documents.services.validators import (
    DocumentValidator,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


@handle_pydantic_validation_error
def create_document(
    command: domain.CreateDocument,
    uow: 'UnitOfWork',
) -> domain.Document:
    with uow.wrap():
        document = domain.DocumentDTO(**asdict(command))

        validator = DocumentValidator(document, uow)
        errors = (
            validator
            .validate_name()
            .validate_library_passport()
            .validate_file_size()
            .get_errors())
        if errors:
            raise DomainValidationError(errors)

        return domain.create_document(document, uow)


@handle_pydantic_validation_error
def update_document(
    command: domain.UpdateDocument,
    uow: 'UnitOfWork',
) -> domain.Document:
    with uow.wrap():
        document = domain.DocumentDTO(**asdict(command))

        validator = DocumentValidator(document, uow)
        errors = (
            validator
            .validate_existence()
            .validate_name()
            .validate_file_size()
            .get_errors()
        )
        if errors:
            raise DomainValidationError(errors)

        return domain.update_document(document, uow)


@handle_pydantic_validation_error
def delete_document(
    command: domain.DeleteDocument,
    uow: 'UnitOfWork',
) -> None:
    with uow.wrap():
        document = domain.DocumentDTO(**asdict(command))

        validator = DocumentValidator(document, uow)
        errors = validator.validate_existence().get_errors()
        if errors:
            raise DomainValidationError(errors)

        domain.delete_document(document, uow)
