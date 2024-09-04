from typing import (
    Union,
)

from pydantic import (
    Field,
)
from pydantic.dataclasses import (
    dataclass,
)


class InstitutionTypeNotFound(Exception):
    """Возбуждается, когда тип организации не может быть определен."""

    def __init__(self, *args):
        super().__init__('Тип организации не найден', *args)


@dataclass
class InstitutionType:
    """Тип организации.

    Является проекцией сущностей внешних ИС.
    """

    id: int = Field(title='Глобальный идентификатор')
    code: Union[str, None] = Field(title='Код', max_length=20)
    name: str = Field(title='Наименование', max_length=200)
