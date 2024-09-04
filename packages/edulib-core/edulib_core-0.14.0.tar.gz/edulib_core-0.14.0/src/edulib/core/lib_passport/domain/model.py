from typing import (
    Optional,
)

from explicit.contrib.domain.model.fields import (
    identifier,
)
from pydantic import (
    Field,
    validator,
)
from pydantic.dataclasses import (
    dataclass,
)


class PassportNotFound(Exception):
    """Возбуждается, когда паспорт библиотеки не может быть определен."""

    def __init__(self, *args):
        super().__init__('Паспорт библиотеки не найден', *args)


class WorkModeNotFound(Exception):
    """Возбуждается, когда режим работы не может быть определен."""

    def __init__(self, *args):
        super().__init__('Режим работы не найден', *args)


@dataclass(config={'validate_assignment': True})
class Passport:
    id: Optional[int] = identifier()
    school_id: int = Field(
        title='Идентификатор ОО',
    )
    name: Optional[str] = Field(
        title='Наименование библиотеки',
        max_length=250,
    )
    date_found_month: Optional[int] = Field(
        title='Дата основания (месяц)',
    )
    date_found_year: Optional[int] = Field(
        title='Дата основания (год)',
    )
    library_chief_id: Optional[int] = Field(
        title='Заведующий библиотекой',
        default=None,
    )
    is_address_match: bool = Field(
        title='Адрес совпадает с адресом ОО',
        default=False,
    )
    is_telephone_match: bool = Field(
        title='Телефон совпадает с телефоном ОО',
        default=False,
    )
    telephone: Optional[str] = Field(
        title='Телефон библиотеки',
        max_length=50,
    )
    is_email_match: bool = Field(
        title='Email совпадает с email ОО',
        default=False,
    )
    email: Optional[str] = Field(
        title='Эл. почта библиотеки',
        max_length=50,
    )
    academic_year_id: Optional[int] = Field(
        title='Период обучения',
        default=None,
    )
    address_id: Optional[int] = Field(
        title='Идентификатор адреса',
        default=None,
    )

    @validator('name')
    def not_empty(cls, value, field):  # pylint: disable=no-self-argument
        if isinstance(value, str) and not value.strip():
            raise ValueError(f'{field.field_info.title} не может быть пустым')
        return value


@dataclass
class WorkMode:
    id: Optional[int] = identifier()
    lib_passport_id: int = Field(
        title='Паспорт библиотеки',
    )
    schedule_mon_from: Optional[str] = Field(
        title='Режим работы с - Понедельник',
        max_length=10,
    )
    schedule_mon_to: Optional[str] = Field(
        title='Режим работы по - Понедельник',
        max_length=10,
    )
    schedule_tue_from: Optional[str] = Field(
        title='Режим работы с - Вторник',
        max_length=10,
    )
    schedule_tue_to: Optional[str] = Field(
        title='Режим работы по - Вторник',
        max_length=10,
    )
    schedule_wed_from: Optional[str] = Field(
        title='Режим работы с - Среда',
        max_length=10,
    )
    schedule_wed_to: Optional[str] = Field(
        title='Режим работы по - Среда',
        max_length=10,
    )
    schedule_thu_from: Optional[str] = Field(
        title='Режим работы с - Четверг',
        max_length=10,
    )
    schedule_thu_to: Optional[str] = Field(
        title='Режим работы по - Четверг',
        max_length=10,
    )
    schedule_fri_from: Optional[str] = Field(
        title='Режим работы с - Пятница',
        max_length=10,
    )
    schedule_fri_to: Optional[str] = Field(
        title='Режим работы по - Пятница',
        max_length=10,
    )
    schedule_sat_from: Optional[str] = Field(
        title='Режим работы с - Суббота',
        max_length=10,
    )
    schedule_sat_to: Optional[str] = Field(
        title='Режим работы по- Суббота',
        max_length=10,
    )
    schedule_sun_from: Optional[str] = Field(
        title='Режим работы с - Воскресенье',
        max_length=10,
    )
    schedule_sun_to: Optional[str] = Field(
        title='Режим работы по - Воскресенье',
        max_length=10,
    )
