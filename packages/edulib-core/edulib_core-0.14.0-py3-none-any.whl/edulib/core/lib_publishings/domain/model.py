from typing import (
    Optional,
)

from explicit.contrib.domain.model import (
    identifier,
)
from pydantic import (
    Field,
    validator,
)
from pydantic.dataclasses import (
    dataclass,
)


class PublishingNotFound(Exception):
    """Возбуждается, когда издательство не может быть определено."""

    def __init__(self, *args):
        super().__init__('Издательство не найдено', *args)


@dataclass(config={'validate_assignment': True})
class Publishing:

    id: Optional[int] = identifier()
    name: str = Field(
        title='Издательство',
        max_length=256,
    )

    @validator('name')
    def not_empty(cls, value, field):  # pylint: disable=no-self-argument
        text = value.strip()
        if text == '':
            raise ValueError(f'{field.field_info.title} не может быть пустым')

        return text
