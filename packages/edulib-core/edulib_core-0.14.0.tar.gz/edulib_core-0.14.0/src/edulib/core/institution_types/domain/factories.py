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
    InstitutionType,
)


class InstitutionTypeDTO(DTOBase):

    id: Union[int, Unset] = unset
    code: Union[str, Unset] = unset
    name: Optional[Union[str, Unset]] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: InstitutionTypeDTO) -> InstitutionType:
        return InstitutionType(**data.dict())


factory = Factory()
