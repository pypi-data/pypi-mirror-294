from typing import (
    TYPE_CHECKING,
)

from .factories import (
    CleanupDayDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .model import (
        CleanupDay,
    )


def create_cleanup_day(data: 'CleanupDayDTO', uow: 'UnitOfWork') -> 'CleanupDay':
    """Сервис создания санитарного дня."""
    cleanup_day = factory.create(data)
    uow.cleanup_days.add(cleanup_day)
    assert cleanup_day.id is not None, cleanup_day

    return cleanup_day


def delete_cleanup_day(data: 'CleanupDayDTO', uow: 'UnitOfWork') -> None:
    """Сервис удаления санитарного дня."""
    cleanup_day = uow.cleanup_days.get_object_by_id(data.id)
    uow.cleanup_days.delete(cleanup_day)
