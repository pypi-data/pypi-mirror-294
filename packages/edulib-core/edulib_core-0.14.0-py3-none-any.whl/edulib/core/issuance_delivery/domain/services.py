from typing import (
    TYPE_CHECKING,
)

from edulib.core.utils.tools import (
    modify,
)

from .factories import (
    IssuanceDeliveryDTO,
    issuance_delivery_factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .model import (
        IssuanceDelivery,
    )



def create_issuance_delivery(data: IssuanceDeliveryDTO, uow: 'UnitOfWork') -> 'IssuanceDelivery':
    issuance_delivery = uow.issuance_deliveries.add(issuance_delivery_factory.create(data))
    assert issuance_delivery.id is not None, issuance_delivery

    return issuance_delivery


def update_issuance_delivery(data: IssuanceDeliveryDTO, uow: 'UnitOfWork') -> 'IssuanceDelivery':
    issuance_delivery = uow.issuance_deliveries.get_object_by_id(data.id)
    modify(issuance_delivery, **data.dict(exclude={'id'}))

    return uow.issuance_deliveries.update(issuance_delivery)
