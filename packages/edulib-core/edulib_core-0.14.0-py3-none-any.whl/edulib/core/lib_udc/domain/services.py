from typing import (
    TYPE_CHECKING,
)

from edulib.core.utils.tools import (
    modify,
)

from .factories import (
    UdcDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .model import (
        Udc,
    )


def create_udc(data: 'UdcDTO', uow: 'UnitOfWork') -> 'Udc':
    """Сервис создания раздела УДК."""
    udc = factory.create(data)
    uow.udc.add(udc)
    assert udc.id is not None, udc

    return udc


def update_udc(data: 'UdcDTO', uow: 'UnitOfWork') -> 'Udc':
    """Сервис обновления раздела УДК."""
    udc = uow.udc.get_object_by_id(data.id)
    modify(udc, **data.dict(exclude={'id'}))
    uow.udc.update(udc)

    return udc


def delete_udc(data: 'UdcDTO', uow: 'UnitOfWork') -> None:
    """Сервис удаления раздела УДК."""
    udc = uow.udc.get_object_by_id(data.id)
    uow.udc.delete(udc)
