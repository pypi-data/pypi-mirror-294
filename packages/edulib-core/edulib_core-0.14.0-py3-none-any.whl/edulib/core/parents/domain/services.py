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
        ParentDTO,
    )
    from .model import (
        Parent,
    )


def create_parent(data: 'ParentDTO', uow: 'UnitOfWork') -> 'Parent':
    parent = factory.create(data)
    uow.parents.add(parent)
    assert parent.id is not None, parent

    return parent


def update_parent(data: 'ParentDTO', uow: 'UnitOfWork') -> 'Parent':
    parent = uow.parents.get_object_by_id(data.id)
    modify(parent, **data.dict(exclude={'id'}))

    return uow.parents.update(parent)


def delete_parent(data: 'ParentDTO', uow: 'UnitOfWork'):
    parent = uow.parents.get_object_by_id(data.id)

    return uow.parents.delete(parent)
