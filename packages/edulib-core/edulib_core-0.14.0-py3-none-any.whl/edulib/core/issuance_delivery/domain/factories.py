from datetime import (
    date,
)
from typing import (
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
from explicit.domain.types import (
    Int,
    NoneInt,
    NoneStr,
)

from .model import (
    IssuanceDelivery,
)


class IssuanceDeliveryDTO(DTOBase):
    id: NoneInt = unset
    issuance_date: Union[date, Unset] = unset
    reader_id: Int = unset
    example_id: Int = unset
    fact_delivery_date: Union[date, None, Unset] = unset
    special_notes: NoneStr = unset
    extension_days_count: NoneInt = unset


class IssuanceDeliveryFactory(AbstractDomainFactory):
    def create(self, data: IssuanceDeliveryDTO) -> IssuanceDelivery:
        return IssuanceDelivery(**data.dict())


issuance_delivery_factory = IssuanceDeliveryFactory()
