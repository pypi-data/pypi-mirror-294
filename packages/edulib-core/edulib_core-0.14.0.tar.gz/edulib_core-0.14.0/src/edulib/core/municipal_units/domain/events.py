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
class MunicipalUnitEvent(Event):

    id: Union[int, Unset] = unset
    name: Union[str, Unset] = unset
    constituent_entity: Union[str, Unset] = unset
    oktmo: Union[str, Unset] = unset


@dataclass
class MunicipalUnitCreated(MunicipalUnitEvent):
    """Муниципальная единица создана."""


@dataclass
class MunicipalUnitUpdated(MunicipalUnitEvent):
    """Муниципальная единица обновлена."""


@dataclass
class MunicipalUnitDeleted(MunicipalUnitEvent):
    """Муниципальная единица удалена."""
