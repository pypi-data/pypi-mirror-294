from datetime import (
    date,
)
from typing import (
    List,
    Union,
)

from explicit.domain import (
    AbstractDomainFactory,
    DTOBase,
    Unset,
    unset,
)

from edulib.core.federal_books.domain.model import (
    FederalBook,
)


class FederalBookDTO(DTOBase):

    id: Union[int, None, Unset] = unset
    name: Union[str, Unset] = unset
    publishing_id: Union[int, Unset] = unset
    pub_lang: Union[str, None, Unset] = unset
    authors: Union[int, Unset] = unset
    parallel_ids: Union[List[int], None, Unset] = unset
    status: Union[bool, None] = True
    code: Union[str, Unset] = unset
    validity_period: Union[date, None, Unset] = unset
    training_manuals: Union[str, None, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: FederalBookDTO) -> FederalBook:
        return FederalBook(**data.dict())


factory = Factory()
