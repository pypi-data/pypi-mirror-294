import datetime
from typing import (
    TYPE_CHECKING,
)

from dateutil.relativedelta import (
    relativedelta,
)

from edulib.core.base.tests.utils import (
    randint,
)
from edulib.core.persons.tests.utils import (
    get_person,
)
from edulib.core.schools.tests.utils import (
    get_school,
)

from ..domain import (
    EmployeeDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from ..domain import (
        Employee,
    )


def get_employee(uow: 'UnitOfWork', save: bool = True, **kwargs) -> 'Employee':

    if 'person_id' not in kwargs:
        kwargs['person_id'] = get_person(uow).id

    if 'school_id' not in kwargs:
        kwargs['school_id'] = get_school(uow).id

    params = {
        'id': randint(),
        'info_date_begin': datetime.date.today() - relativedelta(years=1),
        'info_date_end': None,
        'job_code': 1,
        'job_name': 'Директор',
        'employment_kind_id': 1,
        'personnel_num': '001',
        'object_status': True
    } | kwargs

    employee = factory.create(EmployeeDTO(**params))

    if save:
        employee = uow.employees.add(employee)

    return employee
