from typing import (
    TYPE_CHECKING,
)

from edulib.core.utils.tools import (
    modify,
)

from . import (
    model,
)
from .factories import (
    PassportDTO,
    WorkModeDTO,
    factory,
    work_mode_factory,
)


if TYPE_CHECKING:
    from edulib.core.schools import (
        domain as schools,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from .model import (
        Passport,
        WorkMode,
    )


def create_passport(data: 'PassportDTO', uow: 'UnitOfWork') -> 'Passport':
    """Сервис создания паспорта библиотеки."""
    passport = factory.create(data)
    uow.passports.add(passport)
    assert passport.id is not None, passport

    return passport


def update_passport(data: 'PassportDTO', uow: 'UnitOfWork') -> 'Passport':
    """Сервис обновления паспорта библиотеки."""
    passport = uow.passports.get_object_by_id(data.id)
    modify(passport, **data.dict(exclude={'id'}))
    uow.passports.update(passport)

    return passport


def delete_passport(data: 'PassportDTO', uow: 'UnitOfWork') -> None:
    """Сервис удаления паспорта библиотеки."""
    passport = uow.passports.get_object_by_id(data.id)
    uow.passports.delete(passport)


def create_work_mode(data: 'WorkModeDTO', uow: 'UnitOfWork') -> 'WorkMode':
    """Сервис создания режима работы библиотеки."""
    work_mode = work_mode_factory.create(data)
    uow.work_modes.add(work_mode)
    assert work_mode.id is not None, work_mode

    return work_mode


def update_work_mode(data: 'WorkModeDTO', uow: 'UnitOfWork') -> 'WorkMode':
    """Сервис обновления режима работы библиотеки."""
    work_mode = uow.work_modes.get_object_by_id(data.id)
    modify(work_mode, **data.dict(exclude={'id'}))
    uow.work_modes.update(work_mode)

    return work_mode


def delete_work_mode(data: 'WorkModeDTO', uow: 'UnitOfWork') -> None:
    """Сервис удаления режима работы библиотеки."""
    work_mode = uow.work_modes.get_object_by_id(data.id)
    uow.work_modes.delete(work_mode)


def create_default_passport_for_school(
    school: 'schools.School',
    uow: 'UnitOfWork'
) -> model.Passport:
    """Создает для организации паспорт библиотеки по-умолчанию, если паспорт не существует."""
    try:
        passport = uow.passports.get_by_school_id(school.id)

    except model.PassportNotFound:
        passport = create_passport(
            PassportDTO(
                school_id=school.id,
                name=school.short_name
            ), uow
        )

    return passport
