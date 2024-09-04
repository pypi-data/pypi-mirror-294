from typing import (
    Union,
)

from pydantic import (
    Field,
)
from pydantic.dataclasses import (
    dataclass,
)


class DisciplineNotFound(Exception):

    def __init__(self, *args):
        super().__init__('Предмет не найден', *args)


@dataclass
class Discipline:
    """Предмет.

    Является проекцией сущностей внешних ИС.
    """

    id: int = Field(title='Глобальный идентификатор')
    name: str = Field(title='Наименование', max_length=200)
    description: Union[str, None] = Field(title='Описание')
