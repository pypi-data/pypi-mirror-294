from typing import (
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


class UdcNotFound(Exception):
    """Возбуждается, когда раздел УДК не может быть определен."""

    def __init__(self, *args):
        super().__init__('Раздел УДК не найден', *args)


@dataclass(config={'validate_assignment': True})
class Udc:
    """Раздел УДК."""

    id: Optional[int] = identifier()
    code: str = Field(
        title='Код',
        max_length=32,
    )
    name: str = Field(
        title='Наименование',
        max_length=900,
    )
    parent_id: Optional[int] = Field(
        title='Родительский раздел',
    )

    @validator('code', 'name')
    def not_empty(cls, value, field):  # pylint: disable=no-self-argument
        text = value.strip()
        if text == '':
            raise ValueError(f'{field.field_info.title} не может быть пустым')

        return text
