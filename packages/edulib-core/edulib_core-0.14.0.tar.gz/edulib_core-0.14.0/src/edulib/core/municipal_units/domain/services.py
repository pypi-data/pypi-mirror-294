from typing import (
    TYPE_CHECKING,
)

from edulib.core.utils.tools import (
    modify,
)

from .factories import (
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .factories import (
        MunicipalUnitDTO,
    )
    from .model import (
        MunicipalUnit,
    )


def create_municipal_unit(data: 'MunicipalUnitDTO', uow: 'UnitOfWork') -> 'MunicipalUnit':
    municipal_unit = factory.create(data)

    uow.municipal_units.add(municipal_unit)
    assert municipal_unit.id is not None, municipal_unit

    return municipal_unit


def update_municipal_unit(data: 'MunicipalUnitDTO', uow: 'UnitOfWork') -> 'MunicipalUnit':
    municipal_unit = uow.municipal_units.get_object_by_id(data.id)

    modify(municipal_unit, **data.dict(exclude={'id'}))

    return uow.municipal_units.update(municipal_unit)


def delete_municipal_unit(data: 'MunicipalUnitDTO', uow: 'UnitOfWork'):
    municipal_unit = uow.municipal_units.get_object_by_id(data.id)

    return uow.municipal_units.delete(municipal_unit)
