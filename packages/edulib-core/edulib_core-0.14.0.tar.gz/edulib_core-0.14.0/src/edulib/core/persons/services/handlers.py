from typing import (
    TYPE_CHECKING,
)

from explicit.domain.model import (
    asdict,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
    init_messages_dict,
)

from edulib.core import (
    bus,
    logger,
)
from edulib.core.address import (
    domain as addresses,
)

from .. import (
    domain,
)


if TYPE_CHECKING:
    from explicit.messagebus.events import (
        Event,
    )

    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def null_handler(event: 'Event', uow: 'UnitOfWork') -> None:
    logger.info('Обработка события %s пропущена', type(event))


def on_person_created(
    event: domain.PersonCreated,
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.create_person(domain.PersonDTO(**asdict(event)), uow)


def on_person_updated(
    event: domain.PersonUpdated,
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.update_or_create_person(domain.PersonDTO(**asdict(event)), uow)


def on_person_deleted(
    event: domain.PersonDeleted,
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.delete_person(domain.PersonDTO(**asdict(event)), uow)


def on_address_created(
    event: domain.AddressCreated,
    uow: 'UnitOfWork'
):
    with uow.wrap():
        person = uow.persons.get_object_by_id(event.person_id)

        address = bus.handle(addresses.CreateAddress(**asdict(event)))

        if event.address_type_id == domain.PersonRegistrationType.PERMANENT.value:
            person.perm_reg_addr_id = address.id

        elif event.address_type_id == domain.PersonRegistrationType.TEMPORARY.value:
            person.temp_reg_addr_id = address.id

        else:
            errors = init_messages_dict()
            errors['address_type_id'].append('Неизвестный тип адреса')
            raise DomainValidationError(errors)

        uow.persons.update(person)


def on_address_updated(
    event: domain.AddressUpdated,
    uow: 'UnitOfWork'
):
    with uow.wrap():
        person = uow.persons.get_object_by_id(event.person_id)

        if event.address_type_id == domain.PersonRegistrationType.PERMANENT.value:
            attname = 'perm_reg_addr_id'

        elif event.address_type_id == domain.PersonRegistrationType.TEMPORARY.value:
            attname = 'temp_reg_addr_id'

        else:
            errors = init_messages_dict()
            errors['address_type_id'].append('Неизвестный тип адреса')
            raise DomainValidationError(errors)

        bus.handle(addresses.UpdateAddress(id=getattr(person, attname), **asdict(event)))


def on_address_deleted(
    event: domain.AddressDeleted,
    uow: 'UnitOfWork'
):
    with uow.wrap():
        person = uow.persons.get_object_by_id(event.person_id)

        if event.address_type_id == domain.PersonRegistrationType.PERMANENT.value:
            attname = 'perm_reg_addr_id'

        elif event.address_type_id == domain.PersonRegistrationType.TEMPORARY.value:
            attname = 'temp_reg_addr_id'

        else:
            errors = init_messages_dict()
            errors['address_type_id'].append('Неизвестный тип адреса')
            raise DomainValidationError(errors)

        bus.handle(addresses.DeleteAddress(id=getattr(person, attname), **asdict(event)))
