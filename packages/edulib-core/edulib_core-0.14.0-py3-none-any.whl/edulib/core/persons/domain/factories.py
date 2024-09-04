from typing import (
    Optional,
)

from explicit.domain.factories import (
    AbstractDomainFactory,
    DTOBase,
)
from explicit.domain.model import (
    asdict,
    unset,
)
from explicit.domain.types import (
    Date,
    Int,
    NoneInt,
    NoneStr,
    Str,
)

from .model import (
    Person,
)


class PersonDTO(DTOBase):

    id: Str = unset
    surname: Str = unset
    firstname: Str = unset
    patronymic: NoneStr = unset
    date_of_birth: Date = unset
    inn: NoneStr = unset
    phone: NoneStr = unset
    email: NoneStr = unset
    snils: NoneStr = unset
    gender_id: Int = unset
    perm_reg_addr: NoneInt = unset
    temp_reg_addr: NoneInt = unset

    def get_addresses(self) -> dict:
        return asdict(self, include={'perm_reg_addr', 'temp_reg_addr'})


class AddressDTO(DTOBase):

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


class Factory(AbstractDomainFactory):

    def create(self, data: PersonDTO) -> Person:
        params = data.dict()
        return Person(**params)


factory = Factory()
