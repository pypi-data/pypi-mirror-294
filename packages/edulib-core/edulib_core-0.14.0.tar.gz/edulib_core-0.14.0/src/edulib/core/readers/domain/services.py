from typing import (
    TYPE_CHECKING,
)

from edulib.core.utils.tools import (
    modify,
)

from .factories import (
    ReaderDTO,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .model import (
        Reader,
    )


def update_reader(data: ReaderDTO, uow: 'UnitOfWork') -> 'Reader':
    """Сервис обновления читателя."""
    reader = uow.readers.get_object_by_id(data.id)
    modify(reader, **data.dict(exclude={'id'}))

    return uow.readers.update(reader)
