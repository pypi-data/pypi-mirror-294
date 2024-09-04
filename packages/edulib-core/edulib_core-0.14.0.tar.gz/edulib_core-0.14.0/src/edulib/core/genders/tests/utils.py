import secrets
from typing import (
    TYPE_CHECKING,
)

from edulib.core.base.tests.utils import (
    randint,
)
from edulib.core.genders import (
    domain,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def get_gender(uow: 'UnitOfWork', save: bool = True, **kwargs) -> domain.Gender:
    code, name = secrets.choice(
        (
            ('м.', 'мужской'),
            ('ж.', 'женский'),
        )
    )

    params = {
        'id': randint(),
        'code': code,
        'name': name,
    } | kwargs

    gender = domain.factory.create(domain.GenderDTO(**params))

    if save:
        gender = uow.genders.get_or_create(gender)

    return gender
