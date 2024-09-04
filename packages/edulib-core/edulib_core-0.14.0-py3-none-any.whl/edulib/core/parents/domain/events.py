from explicit.domain.model import (
    unset,
)
from explicit.domain.types import (
    Bool,
    Int,
    Str,
)
from explicit.messagebus.events import (
    Event,
)
from pydantic.dataclasses import (
    dataclass,
)


@dataclass
class ParentEvent(Event):

    id: Int = unset
    parent_person_id: Str = unset
    child_person_id: Str = unset
    parent_type_id: Int = unset
    status: Bool = unset


@dataclass
class ParentCreated(ParentEvent):
    """Представитель создан."""


@dataclass
class ParentUpdated(ParentEvent):
    """Представитель обновлен."""


@dataclass
class ParentDeleted(ParentEvent):
    """Представитель удален."""
