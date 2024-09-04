from typing import (
    TYPE_CHECKING,
)

from ..domain import (
    AddressDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from ..domain import (
        Address,
    )


def get_address(uow: 'UnitOfWork', save: bool = True, **kwargs) -> 'Address':
    params = {
        'full': 'г. Казань, ул. Вымышленная, д. 1',
    } | kwargs

    address = factory.create(AddressDTO(**params))

    if save:
        address = uow.addresses.add(address)

    return address
