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
    StudyLevel,
)


class StudyLevelDTO(DTOBase):

    id: Union[int, Unset] = unset
    name: Union[str, None, Unset] = unset
    short_name: Union[str, None, Unset] = unset
    first_parallel_id: Union[int, Unset] = unset
    last_parallel_id: Union[int, Unset] = unset
    object_status: Union[bool, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: StudyLevelDTO) -> StudyLevel:
        return StudyLevel(**data.dict())


factory = Factory()
