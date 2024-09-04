from typing import (
    TYPE_CHECKING,
)

from explicit.domain.model import (
    asdict,
)

from .. import (
    domain,
)


if TYPE_CHECKING:
    from edulib.core.study_levels.domain import (
        StudyLevelCreated,
        StudyLevelDeleted,
        StudyLevelUpdated,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def on_study_level_created(
    event: 'StudyLevelCreated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.create_study_level(domain.StudyLevelDTO(**asdict(event)), uow)


def on_study_level_updated(
    event: 'StudyLevelUpdated',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.update_study_level(domain.StudyLevelDTO(**asdict(event)), uow)


def on_study_level_deleted(
    event: 'StudyLevelDeleted',
    uow: 'UnitOfWork'
):
    with uow.wrap():
        domain.delete_study_level(domain.StudyLevelDTO(**asdict(event)), uow)
