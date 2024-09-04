from typing import (
    Optional,
    Union,
)

from explicit.domain import (
    Unset,
    unset,
)
from explicit.domain.factories import (
    AbstractDomainFactory,
    DTOBase,
)

from .model import (
    Udc,
)


class UdcDTO(DTOBase):

    id: Optional[int] = None
    code: Union[str, Unset] = unset
    name: Union[str, Unset] = unset
    parent_id: Union[int, None, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: UdcDTO) -> Udc:
        return Udc(**data.dict())


factory = Factory()
