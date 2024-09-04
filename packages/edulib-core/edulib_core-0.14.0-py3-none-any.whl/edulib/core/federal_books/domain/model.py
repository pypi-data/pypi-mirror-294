from datetime import (
    date,
)
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


class FederalBookNotFound(Exception):
    """Возбуждается, когда учебник из Федерального перечня учебников не может быть определен."""

    def __init__(self, *args):
        super().__init__('Учебник из Федерального перечня учебников не найден', *args)


@dataclass(config={'validate_assignment': True})
class FederalBook:

    id: Optional[int] = identifier()
    name: str = Field(title='Наименование', max_length=500,)
    publishing_id: int = Field(title='Издательство',)
    pub_lang: Optional[str] = Field(title='Язык издания', max_length=100,)
    authors: int = Field(title='Автор(ы)',)
    parallel_ids: Optional[list[int]] = Field(title='Параллели')
    status: bool = Field(title='Статус', default=True,)
    code: Optional[str] = Field(title='Код', max_length=50, )
    validity_period: Optional[date] = Field(title='Срок действия')
    training_manuals: Optional[str] = Field(title='Учебные пособия', max_length=1000, )

    class Config:
        title = 'Учебник из Федерального перечня'

    @validator('name', 'authors')
    def not_empty(cls, value, field):  # pylint: disable=no-self-argument
        if isinstance(value, str) and not value.strip():
            raise ValueError(f'{field.field_info.title} не может быть пустым')
        if isinstance(value, int) and value == 0:
            raise ValueError(f'{field.field_info.title} не может быть пустым')
        return value
