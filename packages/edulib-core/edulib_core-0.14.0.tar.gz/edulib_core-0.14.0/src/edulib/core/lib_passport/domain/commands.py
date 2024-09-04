from typing import (
    Union,
)

from explicit.domain import (
    Unset,
    unset,
)
from explicit.messagebus.commands import (
    Command,
)


class CreatePassport(Command):

    school_id: int
    name: str
    date_found_month: Union[int, None, Unset] = unset
    date_found_year: Union[int, None, Unset] = unset
    library_chief_id: Union[int, None, Unset] = unset
    is_address_match: Union[bool, None, Unset] = unset
    is_telephone_match: Union[bool, None, Unset] = unset
    telephone: Union[str, None, Unset] = unset
    is_email_match: Union[bool, None, Unset] = unset
    email: Union[str, None, Unset] = unset
    academic_year_id: Union[int, None, Unset] = unset
    address_id: Union[int, None, Unset] = unset

    class Config:
        title = 'Команда создания паспорта библиотеки'


class UpdatePassport(Command):

    id: int
    name: Union[str, None, Unset] = unset
    date_found_month: Union[int, None, Unset] = unset
    date_found_year: Union[int, None, Unset] = unset
    library_chief_id: Union[int, None, Unset] = unset
    is_address_match: Union[bool, None, Unset] = unset
    is_telephone_match: Union[bool, None, Unset] = unset
    telephone: Union[str, None, Unset] = unset
    is_email_match: Union[bool, None, Unset] = unset
    email: Union[str, None, Unset] = unset
    academic_year_id: Union[int, None, Unset] = unset
    address_id: Union[int, None, Unset] = unset

    class Config:
        title = 'Команда обновления паспорта библиотеки'


class DeletePassport(Command):

    id: int

    class Config:
        title = 'Команда удаления паспорта библиотеки'


class BaseWorkMode(Command):
    schedule_mon_from: Union[str, None, Unset] = unset
    schedule_mon_to: Union[str, None, Unset] = unset
    schedule_tue_from: Union[str, None, Unset] = unset
    schedule_tue_to: Union[str, None, Unset] = unset
    schedule_wed_from: Union[str, None, Unset] = unset
    schedule_wed_to: Union[str, None, Unset] = unset
    schedule_thu_from: Union[str, None, Unset] = unset
    schedule_thu_to: Union[str, None, Unset] = unset
    schedule_fri_from: Union[str, None, Unset] = unset
    schedule_fri_to: Union[str, None, Unset] = unset
    schedule_sat_from: Union[str, None, Unset] = unset
    schedule_sat_to: Union[str, None, Unset] = unset
    schedule_sun_from: Union[str, None, Unset] = unset
    schedule_sun_to: Union[str, None, Unset] = unset

    class Config:
        title = 'Базовая команда режима работы библиотеки'


class CreateWorkMode(BaseWorkMode):

    lib_passport_id: int

    class Config:
        title = 'Команда создания режима работы библиотеки'


class UpdateWorkMode(BaseWorkMode):

    id: int

    class Config:
        title = 'Команда обновления режима работы библиотеки'


class DeleteWorkMode(Command):

    id: int

    class Config:
        title = 'Команда удаления режима работы библиотеки'
