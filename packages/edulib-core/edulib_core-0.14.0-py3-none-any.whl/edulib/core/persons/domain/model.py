import datetime
from typing import (
    Union,
)

from pydantic import (
    Field,
    validator,
)
from pydantic.dataclasses import (
    dataclass,
)

from edulib.core.utils.enums import (
    NamedIntEnum,
)


class PersonNotFound(Exception):

    """Возбуждается, когда физлицо не может быть определено."""

    def __init__(self, *args):
        super().__init__('Физлицо не найдено', *args)


@dataclass(config={
    'json_encoders': {datetime.date: lambda value: value.strftime('%Y-%m-%d')},
    'validate_assignment': True
})
class Person:

    """Физлицо (Персона).

    Является проекцией сущностей внешних ИС.
    """

    id: str = Field(title='Глобальный идентификатор ФЛ', max_length=36)
    surname: str = Field(title='Фамилия', max_length=60)
    firstname: str = Field(title='Имя', max_length=60)
    patronymic: Union[str, None] = Field(title='Отчество', max_length=60, default=None)
    date_of_birth: datetime.date = Field(title='Дата рождения')
    inn: Union[str, None] = Field(title='ИНН', max_length=12, default=None)
    phone: Union[str, None] = Field(title='Мобильный телефон', max_length=50, default=None)
    email: Union[str, None] = Field(title='E-mail', max_length=50, default=None)
    snils: Union[str, None] = Field(title='СНИЛС', max_length=14, default='')
    gender_id: int = Field(title='Пол')
    perm_reg_addr_id: Union[int, None] = Field(title='Адрес регистрации по месту жительства', default=None)
    temp_reg_addr_id: Union[int, None] = Field(title='Адрес регистрации по месту пребывания', default=None)

    @validator('date_of_birth', pre=True)
    def validate_dates(cls, value) -> datetime.date:  # pylint:disable=no-self-argument
        if not value:
            return None

        if isinstance(value, datetime.date):
            return value

        if isinstance(value, str):
            try:
                value = datetime.datetime.strptime(value, "%d.%m.%Y").date()
            except ValueError as exc:
                raise ValueError('Дата должна быть в формате dd.mm.yyyy') from exc

        return value


class PersonRegistrationType(NamedIntEnum):
    """Типы регистрации ФЛ."""

    PERMANENT = 1, 'Регистрация по месту жительства'
    TEMPORARY = 2, 'Регистрация по месту пребывания'
