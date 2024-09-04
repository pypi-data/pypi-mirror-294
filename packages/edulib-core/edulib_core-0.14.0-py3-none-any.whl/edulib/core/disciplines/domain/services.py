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
        DisciplineDTO,
    )
    from .model import (
        Discipline,
    )


def create_discipline(data: 'DisciplineDTO', uow: 'UnitOfWork') -> 'Discipline':
    discipline = factory.create(data)
    uow.disciplines.add(discipline)
    assert discipline.id is not None, discipline

    return discipline


def update_discipline(data: 'DisciplineDTO', uow: 'UnitOfWork') -> 'Discipline':
    discipline = uow.disciplines.get_object_by_id(data.id)
    modify(discipline, **data.dict(exclude={'id'}))

    return uow.disciplines.update(discipline)


def delete_discipline(data: 'DisciplineDTO', uow: 'UnitOfWork'):
    discipline = uow.disciplines.get_object_by_id(data.id)

    return uow.disciplines.delete(discipline)
