from typing import (
    TYPE_CHECKING,
)

from edulib.core.utils.tools import (
    modify,
)

from .factories import (
    DocumentDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .model import (
        Document,
    )


def create_document(data: 'DocumentDTO', uow: 'UnitOfWork') -> 'Document':
    """Сервис создания документа."""
    document = factory.create(data)
    uow.documents.add(document)
    assert document.id is not None, document

    return document


def update_document(data: 'DocumentDTO', uow: 'UnitOfWork') -> 'Document':
    """Сервис обновления документа."""
    document = uow.documents.get_object_by_id(data.id)
    modify(document, **data.dict(exclude={'id'}))
    uow.documents.update(document)

    return document


def delete_document(data: 'DocumentDTO', uow: 'UnitOfWork') -> None:
    """Сервис удаления документа."""
    document = uow.documents.get_object_by_id(data.id)
    uow.documents.delete(document)
