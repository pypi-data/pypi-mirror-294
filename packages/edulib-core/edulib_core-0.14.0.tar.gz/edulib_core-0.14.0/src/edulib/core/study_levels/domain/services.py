from typing import (
    TYPE_CHECKING,
)

from edulib.core.utils.tools import (
    modify,
)

from .factories import (
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .factories import (
        StudyLevelDTO,
    )
    from .model import (
        StudyLevel,
    )


def create_study_level(data: 'StudyLevelDTO', uow: 'UnitOfWork') -> 'StudyLevel':
    study_level = factory.create(data)
    uow.study_levels.add(study_level)
    assert study_level.id is not None, study_level

    return study_level


def update_study_level(data: 'StudyLevelDTO', uow: 'UnitOfWork') -> 'StudyLevel':
    study_level = uow.study_levels.get_object_by_id(data.id)
    modify(study_level, **data.dict(exclude={'id'}))

    return uow.study_levels.update(study_level)


def delete_study_level(data: 'StudyLevelDTO', uow: 'UnitOfWork'):
    study_level = uow.study_levels.get_object_by_id(data.id)

    return uow.study_levels.delete(study_level)
