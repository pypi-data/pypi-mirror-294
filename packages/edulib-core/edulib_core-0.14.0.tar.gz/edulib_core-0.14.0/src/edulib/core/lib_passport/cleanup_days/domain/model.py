from datetime import (
    date,
)
from typing import (
    Optional,
)

from explicit.contrib.domain.model.fields import (
    identifier,
)
from pydantic import (
    Field,
)
from pydantic.dataclasses import (
    dataclass,
)


class CleanupDayNotFound(Exception):
    """Возбуждается, когда санитарный день не может быть определен."""
    def __init__(self, *args):
        super().__init__('Санитарный день не найден', *args)


@dataclass
class CleanupDay:
    id: Optional[int] = identifier()
    cleanup_date: date = Field(
        title='Дата санитарного дня',
    )
    lib_passport_id: int = Field(title='Паспорт библиотеки')
