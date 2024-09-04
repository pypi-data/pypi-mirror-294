from datetime import (
    date,
)
from typing import (
    Optional,
)

from explicit.messagebus.commands import (
    Command,
)


class CreateCleanupDay(Command):

    lib_passport_id: int
    cleanup_date: Optional[date]

    class Config:
        title = 'Команда создания санитарного дня'


class DeleteCleanupDay(Command):

    id: int

    class Config:
        title = 'Команда удаления санитарного дня'
