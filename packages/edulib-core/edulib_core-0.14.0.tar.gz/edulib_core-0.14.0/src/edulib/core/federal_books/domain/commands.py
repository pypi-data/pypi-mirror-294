from datetime import (
    date,
)
from typing import (
    List,
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


class CreateFederalBook(Command):

    name: str
    publishing_id: int
    pub_lang: Optional[str]
    authors: int
    parallel_ids: Union[List[int], None, Unset] = unset
    status: Union[bool, None, Unset] = unset
    code: Optional[str]
    validity_period: Optional[date]
    training_manuals: Optional[str]

    class Config:
        title = 'Команда создания учебника из Федерального перечня учебников'


class UpdateFederalBook(Command):

    id: int
    status: bool

    class Config:
        title = 'Команда обновления учебника из Федерального перечня учебников'
