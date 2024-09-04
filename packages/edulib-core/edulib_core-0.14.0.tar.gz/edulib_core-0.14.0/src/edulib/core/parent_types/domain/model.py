from typing import (
    Union,
)

from pydantic import (
    Field,
)
from pydantic.dataclasses import (
    dataclass,
)


class ParentTypeNotFound(Exception):

    def __init__(self, *args):
        super().__init__('Тип представителя не найден', *args)


@dataclass
class ParentType:
    """Тип представителя.

    Является проекцией сущностей внешних ИС.
    """

    id: int = Field(title='Глобальный идентификатор')
    code: Union[str, None] = Field(title='Код', max_length=20, default=None)
    name: str = Field(title='Наименование', max_length=200)
    status: bool = Field(title='Статус')
