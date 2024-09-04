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

from edulib.core.base.domain import (
    BaseEnumerate,
)


class EmployeeNotFound(Exception):

    def __init__(self, *args):
        super().__init__('Сотрудник не найден', *args)


@dataclass(config={
    'json_encoders': {datetime.date: lambda value: value.strftime('%Y-%m-%d')},
    'validate_assignment': True
})
class Employee:
    """Сотрудник.

    Является проекцией сущностей внешних ИС.
    """

    id: int = Field(title='Глобальный идентификатор')
    person_id: str = Field(title='Физлицо', max_length=36)
    school_id: int = Field(title='Организация')
    personnel_num: Union[str, None] = Field(title='Табельный номер', max_length=100)
    info_date_begin: datetime.date = Field(title='Дата вступления в должность')
    info_date_end: Union[datetime.date, None] = Field(title='Дата выхода из должности', default=None)
    job_code: Union[int, None] = Field(title='Код должности', default=None)
    job_name: Union[str, None] = Field(title='Наименование должности', max_length=200)
    employment_kind_id: int = Field(title='Вид занятости')
    object_status: bool = Field(title='Статус')

    @validator('info_date_begin', 'info_date_end', pre=True)
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


class EmploymentKind(BaseEnumerate):
    PRIMARY = 1
    PART_TIME = 2

    values = {
        PRIMARY: 'Основное место работы',
        PART_TIME: 'Совместительство',
    }
