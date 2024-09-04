from typing import (
    Union,
)

from explicit.domain import (
    Unset,
    unset,
)
from explicit.messagebus.commands import (
    Command,
)


class CreatePublishing(Command):

    name: str

    class Config:
        title = 'Команда создания издательства'


class UpdatePublishing(Command):

    id: int
    name: Union[str, Unset] = unset

    class Config:
        title = 'Команда обновления издательства'


class DeletePublishing(Command):

    id: int

    class Config:
        title = 'Команда удаления издательства'
