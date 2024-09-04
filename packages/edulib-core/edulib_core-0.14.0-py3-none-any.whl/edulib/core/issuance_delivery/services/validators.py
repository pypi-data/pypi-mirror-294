from typing import (
    TYPE_CHECKING,
)

from edulib.core.base.validation import (
    Validator,
    may_skip,
)
from edulib.core.issuance_delivery.domain import (
    IssuanceDeliveryNotFound,
    issuance_delivery_factory,
)
from edulib.core.lib_registry.domain import (
    RegistryExampleNotFound,
)
from edulib.core.readers.domain import (
    ReaderNotFound,
)


if TYPE_CHECKING:
    from explicit.domain import (
        DTOBase,
    )

    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


class IssuanceDeliveryValidator(Validator):
    def __init__(self, data: 'DTOBase', uow: 'UnitOfWork') -> None:
        super().__init__(data, uow)

        self._issuance_delivery = None

    def validate_existence(self) -> 'IssuanceDeliveryValidator':
        try:
            self._issuance_delivery = self._uow.issuance_deliveries.get_object_by_id(self._data.id)
        except IssuanceDeliveryNotFound as exc:
            self._errors['id'].append(str(exc))
            self._skip_chain = True

        return self

    @may_skip
    def validate_issue(self) -> 'IssuanceDeliveryValidator':
        if self._uow.issuance_deliveries.is_issued(issuance_delivery_factory.create(self._data)):
            self._errors['example_id'].append('Экземпляр библиотечного издания уже выдан')

        return self

    def validate_reader(self) -> 'IssuanceDeliveryValidator':
        return self._validate_relation('reader_id', self._uow.readers, ReaderNotFound)

    def validate_example(self) -> 'IssuanceDeliveryValidator':
        return self._validate_relation(
            'example_id',
            self._uow.registry_examples,
            RegistryExampleNotFound,
            skip_chain=True,
        )
