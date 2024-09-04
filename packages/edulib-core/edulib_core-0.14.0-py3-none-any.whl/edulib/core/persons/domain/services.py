from typing import (
    TYPE_CHECKING,
)

from edulib.core.address import (
    domain as addresses,
)
from edulib.core.utils.tools import (
    modify,
)

from . import (
    model,
)
from .factories import (
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .factories import (
        PersonDTO,
    )


def create_person(data: 'PersonDTO', uow: 'UnitOfWork') -> 'model.Person':
    person = factory.create(data)

    uow.persons.add(person)
    assert person.id is not None, person

    for addrname, value in data.get_addresses().items():
        if value is None:
            address_id = value
        else:
            address_id = addresses.create_address(addresses.AddressDTO(full=value), uow).id

        setattr(person, f'{addrname}_id', address_id)

    return uow.persons.update(person)


def update_person(person: 'model.Person', data: 'PersonDTO', uow: 'UnitOfWork'):
    modify(person, **data.dict(exclude={'id'}))

    for addrname, value in data.get_addresses().items():
        try:
            address = uow.addresses.get_object_by_id(getattr(person, f'{addrname}_id'))
        except addresses.AddressNotFound:
            address = None

        if value is None and address is not None:
            addresses.delete_address(address, uow)
            address = None

        elif value is not None and address is None:
            address = addresses.create_address(addresses.AddressDTO(full=value), uow)

        elif value is not None and address is not None and address.full != value:
            addresses.delete_address(address, uow)
            address = addresses.create_address(addresses.AddressDTO(full=value), uow)

        setattr(person, f'{addrname}_id', address.id if address else None)

    return uow.persons.update(person)


def update_or_create_person(data: 'PersonDTO', uow: 'UnitOfWork'):
    assert data.id

    try:
        person = uow.persons.get_object_by_id(data.id)
    except model.PersonNotFound:
        person = create_person(data, uow)
    else:
        person = update_person(person, data, uow)

    return person


def delete_person(data: 'PersonDTO', uow: 'UnitOfWork'):
    assert data.id

    try:
        person = uow.persons.get_object_by_id(data.id)
    except model.PersonNotFound:
        return

    for attname in ('perm_reg_addr_id', 'temp_reg_addr_id'):
        try:
            address = uow.addresses.get_object_by_id(getattr(person, attname))
            addresses.delete_address(address, uow)
        except addresses.AddressNotFound:
            pass

    return uow.persons.delete(person)
