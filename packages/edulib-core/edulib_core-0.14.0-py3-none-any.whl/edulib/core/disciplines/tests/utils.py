import secrets
from typing import (
    TYPE_CHECKING,
)

from edulib.core.base.tests.utils import (
    randint,
)
from edulib.core.disciplines import (
    domain,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def get_discipline(uow: 'UnitOfWork', save: bool = True, **kwargs) -> domain.Discipline:
    names = (
        'Математика',
        'Русский язык',
        'Информатика',
        'Физика',
        'Химия',
    )
    if not (name := kwargs.get('name')):
        name = secrets.choice(names)

    params = {
        'id': randint(),
        'name': name,
    } | kwargs

    discipline = domain.factory.create(domain.DisciplineDTO(**params))

    if save:
        discipline = uow.disciplines.add(discipline)

    return discipline
