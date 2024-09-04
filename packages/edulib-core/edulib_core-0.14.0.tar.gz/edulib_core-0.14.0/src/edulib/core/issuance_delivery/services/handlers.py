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

from edulib.core.issuance_delivery import (
    domain,
)
from edulib.core.issuance_delivery.services.validators import (
    IssuanceDeliveryValidator,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


@handle_pydantic_validation_error
def deliver_examples(
    command: domain.DeliverExamples,
    uow: 'UnitOfWork',
) -> list[domain.IssuanceDelivery]:
    with uow.wrap():
        issuances = []
        for issued_id in command.issued_ids:
            issuance_delivery = domain.IssuanceDeliveryDTO(**asdict(command), id=issued_id)

            validator = IssuanceDeliveryValidator(issuance_delivery, uow)
            errors = validator.validate_existence().get_errors()
            if errors:
                raise DomainValidationError(errors)

            issuances.append(domain.update_issuance_delivery(issuance_delivery, uow))

        return issuances


@handle_pydantic_validation_error
def issue_examples(
    command: domain.IssueExamples,
    uow: 'UnitOfWork',
) -> list[domain.IssuanceDelivery]:
    with uow.wrap():
        issuances = []
        for example_id in command.examples:
            issuance_delivery = domain.IssuanceDeliveryDTO(**asdict(command), example_id=example_id)

            validator = IssuanceDeliveryValidator(issuance_delivery, uow)
            errors = validator.validate_example().validate_reader().validate_issue().get_errors()
            if errors:
                raise DomainValidationError(errors)

            issuances.append(domain.create_issuance_delivery(issuance_delivery, uow))

        return issuances


@handle_pydantic_validation_error
def auto_issue_examples(
    command: domain.AutoIssueExamples,
    uow: 'UnitOfWork',
) -> list[domain.IssuanceDelivery]:
    with uow.wrap():
        issuances = []
        for issuance in command.issued:
            for lib_reg_entry_id in issuance.book_registry_ids:
                examples = uow.registry_examples.get_available_examples(
                    lib_reg_entry_id=lib_reg_entry_id,
                    count=command.count,
                )
                if len(examples) < command.count:
                    raise DomainValidationError(
                        {'__root__': 'Выбраны издания, у которых недостаточное для выдачи количество экземпляров'}
                    )

                for example in examples:
                    issuance_delivery = domain.IssuanceDeliveryDTO(
                        example_id=example.id,
                        reader_id=issuance.reader_id,
                        issuance_date=command.issuance_date,
                    )
                    issuances.append(domain.create_issuance_delivery(issuance_delivery, uow))

        return issuances


@handle_pydantic_validation_error
def prolong_issuance(
    command: domain.ProlongIssuance,
    uow: 'UnitOfWork',
) -> domain.IssuanceDelivery:
    with uow.wrap():
        issuance_delivery = domain.IssuanceDeliveryDTO(**asdict(command))

        validator = IssuanceDeliveryValidator(issuance_delivery, uow)
        errors = validator.validate_existence().get_errors()
        if errors:
            raise DomainValidationError(errors)

        return domain.update_issuance_delivery(issuance_delivery, uow)
