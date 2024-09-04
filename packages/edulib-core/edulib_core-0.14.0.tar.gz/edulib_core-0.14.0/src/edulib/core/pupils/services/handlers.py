from typing import (
    TYPE_CHECKING,
)

from explicit.domain.model import (
    asdict,
)

from edulib.core.persons import (
    domain as persons,
)
from edulib.core.schoolchildren import (
    domain as schoolchildren,
)

from .. import (
    domain,
)


if TYPE_CHECKING:
    from edulib.core.pupils.domain.events import (
        PupilCreated,
        PupilDeleted,
        PupilUpdated,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def on_pupil_created(
    event: 'PupilCreated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        person: persons.Person = uow.persons.get_object_by_id(event.person_id)
        schoolchild: schoolchildren.Schoolchild = schoolchildren.get_or_create_schoolchild(person, uow)

        domain.create_pupil(
            domain.PupilDTO(**asdict(event) | {'schoolchild_id': schoolchild.id, 'class_year_id': event.class_year_id}),
            uow
        )


def on_pupil_updated(
    event: 'PupilUpdated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.update_pupil(domain.PupilDTO(**asdict(event)), uow)


def on_pupil_deleted(
    event: 'PupilDeleted',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.delete_pupil(domain.PupilDTO(**asdict(event)), uow)
