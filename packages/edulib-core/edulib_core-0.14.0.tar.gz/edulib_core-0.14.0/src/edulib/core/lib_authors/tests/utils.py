import secrets
from typing import (
    TYPE_CHECKING,
)

from edulib.core.lib_authors import (
    domain,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def get_author(uow: 'UnitOfWork', save: bool = True, **kwargs) -> domain.Author:
    names = (
        'Бархударов С.Г.',
        'Крючков С.Е.',
        'Максимов Л.Ю.',
        'Буянова Н.А.',
        'Плешаков А.А.',
        'Джулабов У.А., Гелястанова Л.О.',
    )
    if not (name := kwargs.get('name')):
        name = secrets.choice(names)

    params = {'name': name} | kwargs
    author = domain.factory.create(domain.AuthorDTO(**params))

    if save:
        author = uow.authors.add(author)

    return author
