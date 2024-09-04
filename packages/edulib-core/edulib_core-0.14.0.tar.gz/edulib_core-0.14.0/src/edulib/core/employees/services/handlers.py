from typing import (
    TYPE_CHECKING,
)

from explicit.domain.model import (
    asdict,
)

from edulib.core.persons import (
    domain as persons,
)

from .. import (
    domain,
)


if TYPE_CHECKING:
    from edulib.core.employees.domain import (
        EmployeeCreated,
        EmployeeDeleted,
        EmployeeUpdated,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def on_employee_created(
    event: 'EmployeeCreated',
    uow: 'UnitOfWork'
):
    data = asdict(event)

    with uow.wrap():
        try:
            person = uow.persons.get_object_by_id(event.person_id)

        except persons.PersonNotFound:
            person = persons.create_person(
                persons.PersonDTO(**data | {'id': event.person_id}), uow
            )

        else:
            persons.update_person(
                person, persons.PersonDTO(**data | {'id': person.id}), uow
            )

        domain.create_employee(domain.EmployeeDTO(person_id=person.id, **data), uow)


def on_employee_updated(
    event: 'EmployeeUpdated',
    uow: 'UnitOfWork'
):
    data = asdict(event)

    with uow.wrap():
        employee = uow.employees.get_object_by_id(event.id)
        person = uow.persons.get_object_by_id(employee.person_id)

        persons.update_person(person, persons.PersonDTO(**data | {'id': employee.person_id}), uow)
        domain.update_employee(employee, domain.EmployeeDTO(**data), uow)


def on_employee_deleted(
    event: 'EmployeeDeleted',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.delete_employee(domain.EmployeeDTO(**asdict(event)), uow)
