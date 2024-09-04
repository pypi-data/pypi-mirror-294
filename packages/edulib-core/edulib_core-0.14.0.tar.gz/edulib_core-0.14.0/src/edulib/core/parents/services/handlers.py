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
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def on_parent_created(
    event: domain.ParentCreated,
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.create_parent(domain.ParentDTO(**asdict(event)), uow)


def on_parent_updated(
    event: domain.ParentUpdated,
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.update_parent(domain.ParentDTO(**asdict(event)), uow)


def on_parent_deleted(
    event: domain.ParentDeleted,
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.delete_parent(domain.ParentDTO(**asdict(event)), uow)
