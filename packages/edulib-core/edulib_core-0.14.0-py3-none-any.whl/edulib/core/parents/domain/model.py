from pydantic import (
    Field,
)
from pydantic.dataclasses import (
    dataclass,
)


class ParentNotFound(Exception):

    def __init__(self, *args):
        super().__init__('Представитель не найден', *args)


@dataclass
class Parent:
    """Представитель.

    Является проекцией сущностей внешних ИС.
    """

    id: int = Field(title='Глобальный идентификатор')
    parent_person_id: str = Field(title='Представитель', max_length=36)
    child_person_id: str = Field(title='Ученик', max_length=36)
    parent_type_id: int = Field(title='Тип представителя')
    status: bool = Field(title='Статус')
