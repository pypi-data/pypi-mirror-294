from explicit.domain import (
    Bool,
    Date,
    Int,
    NoneDate,
    NoneInt,
    NoneStr,
    unset,
)
from explicit.messagebus.events import (
    Event,
)
from pydantic.dataclasses import (
    dataclass,
)


class EmployeeEvent(Event):

    id: Int = unset
    person_id: Int = unset
    school_id: Int = unset
    info_date_begin: Date = unset
    info_date_end: NoneDate = unset
    job_code: NoneInt = unset
    job_name: NoneStr = unset
    employment_kind_id: Int = unset
    object_status: Bool = unset


@dataclass
class EmployeeCreated(EmployeeEvent):
    """Сотрудник создан."""


@dataclass
class EmployeeUpdated(EmployeeEvent):
    """Сотрудник обновлен."""


@dataclass
class EmployeeDeleted(EmployeeEvent):
    """Сотрудник удален."""
