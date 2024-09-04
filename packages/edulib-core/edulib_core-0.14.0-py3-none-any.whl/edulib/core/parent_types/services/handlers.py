from typing import (
    TYPE_CHECKING,
)

from explicit.domain.model import (
    asdict,
)

from .. import (
    domain,
)


if TYPE_CHECKING:
    from edulib.core.parent_types.domain import (
        ParentTypeCreated,
        ParentTypeDeleted,
        ParentTypeUpdated,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def on_parent_type_created(
    event: 'ParentTypeCreated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.create_parent_type(domain.ParentTypeDTO(**asdict(event)), uow)


def on_parent_type_updated(
    event: 'ParentTypeUpdated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.update_parent_type(domain.ParentTypeDTO(**asdict(event)), uow)


def on_parent_type_deleted(
    event: 'ParentTypeDeleted',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.delete_parent_type(domain.ParentTypeDTO(**asdict(event)), uow)
