from pydantic import (
    Field,
)
from pydantic.dataclasses import (
    dataclass,
)


class ParallelNotFound(Exception):

    def __init__(self, *args):
        super().__init__('Параллель не найдена', *args)


@dataclass
class Parallel:
    """Параллель.

    Является проекцией сущностей внешних ИС.
    """

    id: int = Field(title='Глобальный идентификатор')
    title: str = Field(title='Наименование', max_length=20)
    system_object_id: int = Field(title='Идентификатор')
    object_status: bool = Field(title='Статус')
