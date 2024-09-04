import secrets
from typing import (
    TYPE_CHECKING,
)

from edulib.core.lib_publishings import (
    domain,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def get_publishing(uow: 'UnitOfWork', save: bool = True, **kwargs) -> domain.Publishing:
    names = (
        'АСТ',
        'Эксмо',
        'Москва',
        'Наука',
        'Питер',
    )
    if not (name := kwargs.get('name')):
        name = secrets.choice(names)

    params = {'name': name} | kwargs

    publishing = domain.factory.create(domain.PublishingDTO(**params))

    if save:
        publishing = uow.publishings.add(publishing)

    return publishing
