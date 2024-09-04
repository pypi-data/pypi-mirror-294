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
class StudyLevelEvent(Event):

    id: Union[int, Unset] = unset
    name: Union[str, None, Unset] = unset
    short_name: Union[str, None, Unset] = unset
    first_parallel_id: Union[int, Unset] = unset
    last_parallel_id: Union[int, Unset] = unset
    object_status: Union[bool, Unset] = unset


@dataclass
class StudyLevelCreated(StudyLevelEvent):
    """Уровень обучения создан."""


@dataclass
class StudyLevelUpdated(StudyLevelEvent):
    """Уровень обучения обновлен."""


@dataclass
class StudyLevelDeleted(StudyLevelEvent):
    """Уровень обучения удален."""
