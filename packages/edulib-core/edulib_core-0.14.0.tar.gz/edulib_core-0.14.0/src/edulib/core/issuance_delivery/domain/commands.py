from datetime import (
    date,
)
from typing import (
    Optional,
)

from explicit.messagebus.commands import (
    Command,
)
from pydantic import (  # pylint: disable=no-name-in-module
    BaseModel,
)


class IssueExamples(Command):
    """Команда "Выдать экземпляры"."""

    reader_id: int
    issuance_date: date
    examples: list[int]


class _Issuance(BaseModel):
    reader_id: int
    book_registry_ids: list[int]


class AutoIssueExamples(Command):
    """Команда "Автоматическая выдача экземпляров"."""

    issuance_date: date
    count: int
    issued: list[_Issuance]


class DeliverExamples(Command):
    """Команда "Сдать экземпляры"."""

    issued_ids: list[int]
    fact_delivery_date: date
    special_notes: Optional[str]


class ProlongIssuance(Command):
    """Команда "Продлить выдачу"."""

    id: int
    extension_days_count: int
