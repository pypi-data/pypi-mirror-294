from typing import (
    TYPE_CHECKING,
)

from edulib.core.utils.tools import (
    modify,
)

from . import (
    events,
)
from .factories import (
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .factories import (
        SchoolDTO,
    )
    from .model import (
        School,
    )


def create_school(data: 'SchoolDTO', uow: 'UnitOfWork') -> 'School':
    school = factory.create(data)
    uow.schools.add(school)
    assert school.id is not None, school

    uow.add_event(events.SchoolProjectionCreated(school=school))

    return school


def update_school(data: 'SchoolDTO', uow: 'UnitOfWork') -> 'School':
    school = uow.schools.get_object_by_id(data.id)
    modify(school, **data.dict(exclude={'id'}))

    uow.add_event(events.SchoolProjectionUpdated(school=school))

    return uow.schools.update(school)


def delete_school(data: 'SchoolDTO', uow: 'UnitOfWork'):
    school = uow.schools.get_object_by_id(data.id)

    return uow.schools.delete(school)
