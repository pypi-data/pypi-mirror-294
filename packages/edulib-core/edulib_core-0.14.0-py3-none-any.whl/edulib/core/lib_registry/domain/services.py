from datetime import (
    datetime,
)
from typing import (
    TYPE_CHECKING,
)

from explicit.domain import (
    asdict,
)

from edulib.core.utils.tools import (
    modify,
)

from .factories import (
    RegistryEntryDTO,
    RegistryExampleDTO,
    entry_factory,
    example_factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .model import (
        RegistryEntry,
        RegistryExample,
    )


def create_registry_entry(data: RegistryEntryDTO, uow: 'UnitOfWork') -> 'RegistryEntry':
    """Сервис создания библиотечного издания."""
    registry_entry = entry_factory.create(data)

    if registry_entry.federal_book_id:
        federal_book = uow.federal_books.get_object_by_id(registry_entry.federal_book_id)
        registry_entry.author_id = federal_book.authors
        registry_entry.title = federal_book.name
        registry_entry.parallel_ids = federal_book.parallel_ids

    return uow.registry_entries.add(registry_entry)


def update_registry_entry(data: RegistryEntryDTO, uow: 'UnitOfWork') -> 'RegistryEntry':
    """Сервис обновления библиотечного издания."""
    registry_entry = uow.registry_entries.get_object_by_id(data.id)

    modify(registry_entry, **data.dict(exclude={'id'}))
    if data.federal_book_id:
        federal_book = uow.federal_books.get_object_by_id(data.federal_book_id)
        registry_entry.author_id = federal_book.authors
        registry_entry.title = federal_book.name
        registry_entry.parallel_ids = federal_book.parallel_ids

    return uow.registry_entries.update(registry_entry)


def delete_registry_entry(data: RegistryEntryDTO, uow: 'UnitOfWork') -> None:
    """Сервис удаления библиотечного издания."""
    registry_entry = uow.registry_entries.get_object_by_id(data.id)
    uow.registry_entries.delete(registry_entry)


def create_registry_example(data: RegistryExampleDTO, uow: 'UnitOfWork') -> 'RegistryExample':
    """Сервис создания экземпляра библиотечного издания."""
    registry_example = example_factory.create(data)

    return uow.registry_examples.add(registry_example)


def update_registry_example(data: RegistryExampleDTO, uow: 'UnitOfWork') -> 'RegistryExample':
    """Сервис обновления экземпляра библиотечного издания."""
    registry_example = uow.registry_examples.get_object_by_id(data.id)
    modify(registry_example, **data.dict(exclude={'id'}))

    return uow.registry_examples.update(registry_example)


def delete_registry_example(data: RegistryExampleDTO, uow: 'UnitOfWork') -> None:
    """Сервис удаления экземпляра библиотечного издания."""
    registry_example = uow.registry_examples.get_object_by_id(data.id)
    uow.registry_examples.delete(registry_example)


def copy_registry_example(data: RegistryExampleDTO, uow: 'UnitOfWork') -> None:
    """Сервис копирования экземпляра библиотечного издания."""
    registry_example = uow.registry_examples.get_object_by_id(data.id)

    count = uow.registry_examples.examples_count(registry_example)
    current_year = datetime.now().year

    for index in range(data.count_for_copy):
        copy = asdict(registry_example, exclude=['id'])
        copy['card_number'] = f'{current_year}-{count + index + 1:03}'
        example = example_factory.create(RegistryExampleDTO(**copy))

        uow.registry_examples.add(example)
