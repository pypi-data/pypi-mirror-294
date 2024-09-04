from datetime import (
    datetime,
)
from typing import (
    Optional,
)

from explicit.contrib.domain.model import (
    identifier,
)
from pydantic import (
    Field,
)
from pydantic.dataclasses import (
    dataclass,
)

from edulib.core.utils.enums import (
    NamedIntEnum,
)


class ReaderNotFound(Exception):
    """Возбуждается, когда читатель не может быть определен."""

    def __init__(self, *args):
        super().__init__('Читатель не найден', *args)


class ReaderRole(NamedIntEnum):
    """Роль читателя."""

    STUDENT = 1, 'Ученик'
    TEACHER = 2, 'Сотрудник'
    ALL = 3, 'Все'


@dataclass
class Reader:
    """Читатель."""

    id: Optional[int] = identifier()
    number: Optional[str] = Field(
        title='Номер билета',
        max_length=15,
    )
    schoolchild_id: Optional[int] = Field(
        title='Учащийся',
    )
    teacher_id: Optional[int] = Field(
        title='Сотрудник',
    )
    school_id: Optional[int] = Field(
        title='Образовательная организация',
    )
    year: str = Field(
        title='Дата регистрации в библиотеке',
        max_length=4,
        default_factory=lambda: str(datetime.today().year),
    )
    role: ReaderRole = Field(
        title='Роль',
    )
