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
    from edulib.core.disciplines.domain import (
        DisciplineCreated,
        DisciplineDeleted,
        DisciplineUpdated,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def on_discipline_created(
    event: 'DisciplineCreated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.create_discipline(domain.DisciplineDTO(**asdict(event)), uow)


def on_discipline_updated(
    event: 'DisciplineUpdated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.update_discipline(domain.DisciplineDTO(**asdict(event)), uow)


def on_discipline_deleted(
    event: 'DisciplineDeleted',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.delete_discipline(domain.DisciplineDTO(**asdict(event)), uow)
