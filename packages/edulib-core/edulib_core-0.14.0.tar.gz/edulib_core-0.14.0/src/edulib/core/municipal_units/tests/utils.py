from typing import (
    TYPE_CHECKING,
)

from edulib.core.base.tests.utils import (
    randint,
)

from ..domain import (
    MunicipalUnitDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from ..domain import (
        MunicipalUnit,
    )


def get_municipal_unit(uow: 'UnitOfWork', save: bool = True, **kwargs) -> 'MunicipalUnit':
    params = {
        'id': randint(),
        'name': 'городской округ Казань',
        'constituent_entity': 'Городские округа Республики Татарстан (Татарстана)',
        'oktmo': '92 700 000',
    } | kwargs

    municipal_unit = factory.create(MunicipalUnitDTO(**params))

    if save:
        municipal_unit = uow.municipal_units.add(municipal_unit)

    return municipal_unit
