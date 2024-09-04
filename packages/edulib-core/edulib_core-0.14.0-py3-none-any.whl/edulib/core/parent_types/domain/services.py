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
        ParentTypeDTO,
    )
    from .model import (
        ParentType,
    )


def create_parent_type(data: 'ParentTypeDTO', uow: 'UnitOfWork') -> 'ParentType':
    parent_type = factory.create(data)
    uow.parent_types.add(parent_type)
    assert parent_type.id is not None, parent_type

    return parent_type


def update_parent_type(data: 'ParentTypeDTO', uow: 'UnitOfWork') -> 'ParentType':
    parent_type = uow.parent_types.get_object_by_id(data.id)
    modify(parent_type, **data.dict(exclude={'id'}))

    return uow.parent_types.update(parent_type)


def delete_parent_type(data: 'ParentTypeDTO', uow: 'UnitOfWork'):
    parent_type = uow.parent_types.get_object_by_id(data.id)

    return uow.parent_types.delete(parent_type)
