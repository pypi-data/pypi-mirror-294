from datetime import (
    date,
)
from typing import (
    TYPE_CHECKING,
)

from edulib.core.base.tests.utils import (
    randint,
    randstr,
)
from edulib.core.federal_books import (
    domain,
)
from edulib.core.lib_authors.tests.utils import (
    get_author,
)
from edulib.core.lib_publishings.tests.utils import (
    get_publishing,
)
from edulib.core.parallels.tests.utils import (
    get_parallel,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def get_fed_book(uow: 'UnitOfWork', save: bool = True, **kwargs) -> domain.FederalBook:
    if not (publishing_id := kwargs.get('publishing_id')):
        publishing_id = get_publishing(uow, save=save).id

    if not (author_id := kwargs.get('author_id')):
        author_id = get_author(uow, save=save).id

    if not (parallel_id := kwargs.get('parallel_id')):
        parallel_id = get_parallel(uow, save=save).id

    params = {
        'id': randint(),
        'name': randstr(domain.FederalBook.name.max_length),
        'publishing_id': publishing_id,
        'pub_lang': 'Русский',
        'authors': author_id,
        'parallel_ids': [parallel_id],
        'status': True,
        'code': randstr(domain.FederalBook.code.max_length),
        'validity_period': date.today(),
        'training_manuals': randstr(domain.FederalBook.training_manuals.max_length),
    } | kwargs

    fed_book = domain.factory.create(domain.FederalBookDTO(**params))

    if save:
        fed_book = uow.federal_books.add(fed_book)

    return fed_book
