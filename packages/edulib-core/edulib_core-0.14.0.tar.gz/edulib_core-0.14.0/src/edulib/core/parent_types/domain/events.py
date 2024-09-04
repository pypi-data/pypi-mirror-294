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
class ParentTypeEvent(Event):

    id: Union[int, Unset] = unset
    code: Union[str, None, Unset] = unset
    name: Union[str, Unset] = unset
    status: Union[bool, Unset] = unset


@dataclass
class ParentTypeCreated(ParentTypeEvent):
    """Тип представителя создан."""


@dataclass
class ParentTypeUpdated(ParentTypeEvent):
    """Тип представителя обновлен."""


@dataclass
class ParentTypeDeleted(ParentTypeEvent):
    """Тип представителя удален."""
