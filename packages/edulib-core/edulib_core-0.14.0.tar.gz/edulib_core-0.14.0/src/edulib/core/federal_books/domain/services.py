from typing import (
    TYPE_CHECKING,
)

from edulib.core.federal_books.domain.factories import (
    FederalBookDTO,
    factory,
)
from edulib.core.utils.tools import (
    modify,
)


if TYPE_CHECKING:
    from edulib.core.federal_books.domain.model import (
        FederalBook,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def create_federal_book(data: FederalBookDTO, uow: 'UnitOfWork') -> 'FederalBook':
    """Сервис создания учебника из Федерального перечня учебников."""
    federal_book = factory.create(data)
    uow.federal_books.add(federal_book)
    assert federal_book.id is not None, federal_book

    return federal_book


def update_federal_book(data: FederalBookDTO, uow: 'UnitOfWork') -> 'FederalBook':
    """Сервис обновления учебника из Федерального перечня учебников."""
    federal_book = uow.federal_books.get_object_by_id(data.id)
    modify(federal_book, **data.dict(exclude={'id'}))
    uow.federal_books.update(federal_book)

    return federal_book
