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
    NoneInt,
    NoneStr,
    Str,
)

from .model import (
    Reader,
    ReaderRole,
)


class ReaderDTO(DTOBase):
    id: NoneInt = unset
    number: NoneStr = unset
    schoolchild_id: NoneInt = unset
    teacher_id: NoneInt = unset
    school_id: NoneInt = unset
    year: Str = unset
    role: Union[ReaderRole, Unset]  = unset


class ReaderFactory(AbstractDomainFactory):
    def create(self, data: ReaderDTO) -> Reader:
        return Reader(**data.dict())


reader_factory = ReaderFactory()
