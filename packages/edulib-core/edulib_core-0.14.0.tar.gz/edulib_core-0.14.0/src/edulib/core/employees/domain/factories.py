import datetime
from typing import (
    Union,
)

from explicit.domain.factories import (
    AbstractDomainFactory,
    DTOBase,
)
from explicit.domain.model import (
    Unset,
    unset,
)

from .model import (
    Employee,
)


class EmployeeDTO(DTOBase):

    id: Union[int, Unset] = unset
    info_date_begin: Union[datetime.date, Unset] = unset
    info_date_end: Union[datetime.date, None, Unset] = unset
    person_id: Union[int, Unset] = unset
    school_id: Union[int, Unset] = unset
    job_code: Union[int, None, Unset] = unset
    job_name: Union[str, None, Unset] = unset
    employment_kind_id: Union[int, Unset] = unset
    personnel_num: Union[str, None, Unset] = unset
    object_status: Union[bool, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: EmployeeDTO) -> Employee:
        return Employee(**data.dict())


factory = Factory()
