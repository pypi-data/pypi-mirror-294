from typing import (
    TYPE_CHECKING,
    Union,
)

from edulib.core.utils.tools import (
    modify,
)

from .factories import (
    factory,
)
from .model import (
    EmployeeNotFound,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .factories import (
        EmployeeDTO,
    )
    from .model import (
        Employee,
    )


def create_employee(data: 'EmployeeDTO', uow: 'UnitOfWork') -> 'Employee':
    employee = factory.create(data)
    uow.employees.add(employee)
    assert employee.id is not None, employee

    return employee


def update_employee(employee: 'Employee', data: 'EmployeeDTO', uow: 'UnitOfWork') -> 'Employee':
    modify(employee, **data.dict(exclude={'id'}))

    return uow.employees.update(employee)


def update_or_create_employee(data: 'EmployeeDTO', uow: 'UnitOfWork') -> 'Employee':
    assert data.id

    try:
        employee = uow.employees.get_object_by_id(data.id)
    except EmployeeNotFound:
        employee = create_employee(data, uow)
    else:
        employee = update_employee(employee, data, uow)

    return employee


def delete_employee(data: Union['Employee', 'EmployeeDTO'], uow: 'UnitOfWork'):
    employee = uow.employees.get_object_by_id(data.id)

    return uow.employees.delete(employee)
