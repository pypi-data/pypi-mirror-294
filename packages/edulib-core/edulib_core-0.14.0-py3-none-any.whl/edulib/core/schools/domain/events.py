from typing import (
    Union,
)

from explicit.domain.model import (
    Unset,
    asdict,
    unset,
)
from explicit.messagebus.events import (
    Event,
)
from pydantic.dataclasses import (
    dataclass,
)

from . import (
    model,
)


@dataclass
class SchoolEvent(Event):

    id: Union[int, Unset] = unset
    name: Union[str, None, Unset] = unset
    short_name: Union[str, Unset] = unset
    manager: Union[str, None, Unset] = unset
    status: Union[bool, Unset] = unset
    inn: Union[str, None, Unset] = unset
    kpp: Union[str, None, Unset] = unset
    okato: Union[str, None, Unset] = unset
    oktmo: Union[str, None, Unset] = unset
    okpo: Union[str, None, Unset] = unset
    ogrn: Union[str, None, Unset] = unset
    institution_type_id: Union[int, None, Unset] = unset
    f_address: Union[str, None, Unset] = unset
    u_address: Union[str, None, Unset] = unset
    telephone: Union[str, None, Unset] = unset
    fax: Union[str, None, Unset] = unset
    email: Union[str, None, Unset] = unset
    website: Union[str, None, Unset] = unset
    parent_id: Union[int, None, Unset] = unset
    territory_type_id: Union[int, None, Unset] = unset
    municipal_unit_id: Union[int, None, Unset] = unset

    def get_addresses_data(self):
        return asdict(self, include={'f_address', 'u_address'})


@dataclass
class SchoolCreated(SchoolEvent):
    """Организация создана."""


@dataclass
class SchoolUpdated(SchoolEvent):
    """Организация обновлена."""


@dataclass
class SchoolDeleted(SchoolEvent):
    """Организация удалена."""


@dataclass
class SchoolProjectionEvent(Event):
    """Абстрактное событие проекции организации."""

    school: Union[model.School, Unset] = unset


@dataclass
class SchoolProjectionCreated(SchoolProjectionEvent):
    """Проекция создана."""


@dataclass
class SchoolProjectionUpdated(SchoolProjectionEvent):
    """Проекция обновлена."""


@dataclass
class SchoolProjectionDeleted(SchoolProjectionEvent):
    """Проекция удалена."""
