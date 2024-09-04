from typing import (
    Optional,
)

from explicit.domain.model import (
    unset,
)
from explicit.domain.types import (
    Int,
    NoneStr,
    Str,
)
from explicit.messagebus.events import (
    Event,
)
from pydantic.dataclasses import (
    dataclass,
)


@dataclass
class AbstractPersonAddressEvent(Event):

    id: NoneStr = unset
    place: NoneStr = unset
    street: NoneStr = unset
    house: NoneStr = unset
    house_num: NoneStr = unset
    house_corps: NoneStr = unset
    flat: NoneStr = unset
    full: NoneStr = unset
    zip_code: NoneStr = unset
    person_id: Optional[Str] = unset
    address_type_id: Int = unset


@dataclass
class AddressCreated(AbstractPersonAddressEvent):
    """Адрес ФЛ создан."""


@dataclass
class AddressUpdated(AbstractPersonAddressEvent):
    """Адрес ФЛ изменен."""


@dataclass
class AddressDeleted(AbstractPersonAddressEvent):
    """Адрес ФЛ удален."""
