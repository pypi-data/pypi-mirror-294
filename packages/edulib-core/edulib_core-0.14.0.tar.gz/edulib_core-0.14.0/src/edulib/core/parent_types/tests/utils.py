from typing import (
    TYPE_CHECKING,
)

from edulib.core.base.tests.utils import (
    randint,
)

from ..domain import (
    ParentType,
    ParentTypeDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def get_parent_type(uow: 'UnitOfWork', save: bool = True, **kwargs) -> ParentType:
    params = {
        'id': randint(),
        'name': 'Родитель',
        'status': True,
    } | kwargs

    parent_type = factory.create(ParentTypeDTO(**params))

    if save:
        parent_type = uow.parent_types.add(parent_type)

    return parent_type
