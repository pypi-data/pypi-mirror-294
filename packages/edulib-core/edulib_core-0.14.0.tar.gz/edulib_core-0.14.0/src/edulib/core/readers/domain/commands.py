from explicit.domain import (
    unset,
)
from explicit.domain.types import (
    NoneStr,
)
from explicit.messagebus.commands import (
    Command,
)


class UpdateReader(Command):
    id: int
    number: NoneStr = unset

    class Config:
        title = 'Команда обновления читателя'
