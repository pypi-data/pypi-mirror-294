from typing import (
    Union,
)

from explicit.domain.model import (
    Unset,
    unset,
)
from explicit.messagebus.events import (
    Event,
)
from pydantic.dataclasses import (
    dataclass,
)


@dataclass
class DisciplineEvent(Event):

    id: Union[str, Unset] = unset
    name: Union[str, Unset] = unset
    description: Union[str, None, Unset] = unset


@dataclass
class DisciplineCreated(DisciplineEvent):
    """Предмет создан."""


@dataclass
class DisciplineUpdated(DisciplineEvent):
    """Предмет обновлен."""


@dataclass
class DisciplineDeleted(DisciplineEvent):
    """Предмет удален."""
