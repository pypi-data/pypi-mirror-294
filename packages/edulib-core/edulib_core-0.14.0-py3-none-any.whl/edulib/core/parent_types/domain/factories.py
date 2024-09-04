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
    ParentType,
)


class ParentTypeDTO(DTOBase):

    id: Union[int, Unset] = unset
    code: Union[str, None, Unset] = unset
    name: Union[str, Unset] = unset
    status: Union[bool, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: ParentTypeDTO) -> ParentType:
        return ParentType(**data.dict())


factory = Factory()
