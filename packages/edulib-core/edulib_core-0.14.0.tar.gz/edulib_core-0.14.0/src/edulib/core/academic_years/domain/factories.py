from typing import (
    Optional,
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
    AcademicYear,
)


class AcademicYearDTO(DTOBase):

    id: Union[int, Unset] = unset
    code: Union[str, Unset] = unset
    name: Optional[Union[str, Unset]] = unset
    date_begin: Union[str, Unset] = unset
    date_end: Union[str, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: AcademicYearDTO) -> AcademicYear:
        return AcademicYear(**data.dict())


factory = Factory()
