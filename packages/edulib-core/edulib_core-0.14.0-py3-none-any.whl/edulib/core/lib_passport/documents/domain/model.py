from typing import (
    Any,
    Optional,
)

from explicit.contrib.domain.model.fields import (
    identifier,
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


class DocumentNotFound(Exception):
    """Возбуждается, когда документ не может быть определен."""

    def __init__(self, *args):
        super().__init__('Документ не найден', *args)


class DocumentType(NamedIntEnum):
    """Тип документа"""

    LEGAL = 1, 'Нормативно-правовая база'
    ACCOUNT = 2, 'Документы учета работы библиотеки'


@dataclass
class Document:
    id: Optional[int] = identifier()
    library_passport_id: int = Field(
        title='Паспорт библиотеки',
    )
    doc_type: int = Field(
        title='Тип документа',
    )
    name: Optional[str] = Field(
        title='Наименование',
        max_length=250,
    )
    document: Any = Field(
        title='Файл',
    )

    @validator('name')
    def not_empty(cls, value, field):  # pylint: disable=no-self-argument
        if isinstance(value, str) and not value.strip():
            raise ValueError(f'{field.field_info.title} не может быть пустым')
        return value
