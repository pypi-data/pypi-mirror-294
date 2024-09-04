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
    Discipline,
)


class DisciplineDTO(DTOBase):

    id: Union[str, Unset] = unset
    name: Union[str, Unset] = unset
    description: Union[str, None, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: DisciplineDTO) -> Discipline:
        return Discipline(**data.dict())


factory = Factory()
