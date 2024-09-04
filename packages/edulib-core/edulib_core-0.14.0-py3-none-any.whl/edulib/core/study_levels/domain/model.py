from typing import (
    Union,
)

from pydantic import (
    Field,
)
from pydantic.dataclasses import (
    dataclass,
)


class StudyLevelNotFound(Exception):

    def __init__(self, *args):
        super().__init__('Уровень обучения не найден', *args)


@dataclass
class StudyLevel:
    """Уровень обучения.

    Является проекцией сущностей внешних ИС.
    """

    id: int = Field(title='Глобальный идентификатор')
    name: Union[str, None] = Field(title='Наименование', max_length=200, default=None)
    short_name: Union[str, None] = Field(title='Краткое наименование', max_length=200, default=None)
    first_parallel_id: int = Field(title='Начальная параллель')
    last_parallel_id: int = Field(title='Конечная параллель')
    object_status: bool = Field(title='Статус')
