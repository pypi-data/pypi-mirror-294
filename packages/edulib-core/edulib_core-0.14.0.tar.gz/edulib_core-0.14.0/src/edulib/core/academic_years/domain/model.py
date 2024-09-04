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


class AcademicYearNotFound(Exception):
    """Возбуждается, когда учебный год не может быть определен."""

    def __init__(self, *args):
        super().__init__('Учебный год не найден', *args)


@dataclass(config={
    'json_encoders': {datetime.date: lambda value: value.strftime('%Y-%m-%d')},
    'validate_assignment': True
})
class AcademicYear:
    """Учебный год.

    Является проекцией сущностей внешних ИС.
    """

    id: int = Field(title='Глобальный идентификатор')
    code: str = Field(title='Код', max_length=50)
    name: Union[str, None] = Field(title='Наименование', max_length=200)
    date_begin: datetime.date = Field(title='Дата начала')
    date_end: datetime.date = Field(title='Дата окончания')

    @validator('date_begin', 'date_end', pre=True)
    def validate_dates(cls, value) -> datetime.date:  # pylint:disable=no-self-argument
        if isinstance(value, datetime.date):
            return value

        if isinstance(value, str):
            try:
                value = datetime.datetime.strptime(value, '%d.%m.%Y').date()
            except ValueError as exc:
                raise ValueError('Дата должна быть в формате dd.mm.yyyy') from exc

        return value
