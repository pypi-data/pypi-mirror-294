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
    Schoolchild,
)


class SchoolchildDTO(DTOBase):

    id: Union[int, None, Unset] = unset
    person_id: Union[str, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: SchoolchildDTO) -> Schoolchild:
        params = data.dict()
        return Schoolchild(**params)


factory = Factory()
