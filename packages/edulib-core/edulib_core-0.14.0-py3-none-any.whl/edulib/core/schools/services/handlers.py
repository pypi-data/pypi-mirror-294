from typing import (
    TYPE_CHECKING,
)

from explicit.domain.model import (
    asdict,
)

from edulib.core import (
    bus,
)
from edulib.core.address import (
    domain as addresses,
)

from .. import (
    domain,
)


if TYPE_CHECKING:
    from edulib.core.schools.domain import (
        SchoolCreated,
        SchoolDeleted,
        SchoolUpdated,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def on_school_created(
    event: 'SchoolCreated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        data = asdict(event)

        addresses_data = {}
        for address_name, address_full in event.get_addresses_data().items():
            addresses_data[f'{address_name}_id'] = (
                bus.handle(addresses.CreateAddress(full=address_full)).id
                if address_full is not None else None
            )

        domain.create_school(
            domain.SchoolDTO(**data | addresses_data),
            uow
        )


def on_school_updated(
    event: 'SchoolUpdated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        data = asdict(event)
        addresses_data = {}

        school = uow.schools.get_object_by_id(event.id)

        # Обновить адреса
        for address_name, address_full in event.get_addresses_data().items():
            address_id = getattr(school, f'{address_name}_id', None)
            command = (
                addresses.UpdateAddress(id=address_id, full=address_full)
                if address_id is not None else
                addresses.CreateAddress(full=address_full)
            )
            addresses_data[f'{address_name}_id'] = (
                bus.handle(command).id
                if address_full is not None
                else None
            )

        domain.update_school(
            domain.SchoolDTO(**data | addresses_data),
            uow
        )


def on_school_deleted(
    event: 'SchoolDeleted',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        school = uow.schools.get_object_by_id(event.id)

        for address_name in event.get_addresses_data():
            address_id = getattr(school, f'{address_name}_id', None)
            if address_id:
                bus.handle(addresses.DeleteAddress(id=address_id))

        domain.delete_school(domain.SchoolDTO(**asdict(event)), uow)
