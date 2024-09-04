from datetime import (
    date,
)
from typing import (
    Union,
)

from explicit.domain import (
    AbstractDomainFactory,
    DTOBase,
    Unset,
    unset,
)

from edulib.core.lib_passport.cleanup_days.domain.model import (
    CleanupDay,
)


class CleanupDayDTO(DTOBase):

    id: Union[int, None, Unset] = unset
    cleanup_date: Union[date, None, Unset] = unset
    lib_passport_id: Union[int, None, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: CleanupDayDTO) -> CleanupDay:
        return CleanupDay(**data.dict())


factory = Factory()
