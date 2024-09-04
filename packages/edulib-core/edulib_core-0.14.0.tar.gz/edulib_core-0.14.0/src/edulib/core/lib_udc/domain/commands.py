from typing import (
    Optional,
    Union,
)

from explicit.domain import (
    Unset,
    unset,
)
from explicit.messagebus.commands import (
    Command,
)


class CreateUdc(Command):

    code: str
    name: str
    parent_id: Optional[int]

    class Config:
        title = 'Команда создания раздела УДК'


class UpdateUdc(Command):

    id: int
    code: Union[str, Unset] = unset
    name: Union[str, Unset] = unset
    parent_id: Union[int, None, Unset] = unset

    class Config:
        title = 'Команда обновления раздела УДК'


class DeleteUdc(Command):

    id: int

    class Config:
        title = 'Команда удаления раздела УДК'
