from explicit.domain.factories import (
    AbstractDomainFactory,
    DTOBase,
)
from explicit.domain.model import (
    unset,
)
from explicit.domain.types import (
    Bool,
    Int,
    Str,
)

from .model import (
    Parent,
)


class ParentDTO(DTOBase):

    id: Int = unset
    parent_person_id: Str = unset
    child_person_id: Str = unset
    parent_type_id: Int = unset
    status: Bool = unset


class Factory(AbstractDomainFactory):

    def create(self, data: ParentDTO) -> Parent:
        return Parent(**data.dict())


factory = Factory()
