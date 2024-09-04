from datetime import (
    date,
)
from decimal import (
    Decimal,
)
from typing import (
    Optional,
    Union,
)

from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
)
from explicit.domain import (
    Unset,
    unset,
)
from explicit.messagebus.commands import (
    Command,
)
from pydantic import (  # pylint: disable=no-name-in-module
    PositiveInt,
)

from .model import (
    EntryStatus,
    FinSource,
)


class CreateRegistryEntry(Command):
    type_id: int
    title: Optional[str]
    author_id: Optional[int]
    parallel_ids: Optional[list[int]]
    author_sign: Optional[str]
    udc_id: Optional[int]
    bbc_id: Optional[int]
    tags: Optional[str]
    source_id: Optional[int]
    short_info: Optional[str]
    on_balance: bool
    school_id: int
    filename: Optional[InMemoryUploadedFile]
    cover: Optional[InMemoryUploadedFile]
    discipline_id: Optional[int]
    age_tag_id: Optional[int]
    status: EntryStatus = EntryStatus.CURRENT
    federal_book_id: Optional[int]

    class Config:
        title = 'Команда создания библиотечного издания'
        arbitrary_types_allowed = True


class UpdateRegistryEntry(Command):
    id: int
    type_id: Union[int, Unset] = unset
    title: Union[str, Unset, None] = unset
    author_id: Union[int, Unset, None] = unset
    parallel_ids: Union[list[int], Unset, None] = unset
    author_sign: Union[str, Unset, None] = unset
    udc_id: Union[int, Unset, None] = unset
    bbc_id: Union[int, Unset, None] = unset
    tags: Union[str, Unset, None] = unset
    source_id: Union[int, Unset, None] = unset
    short_info: Union[str, Unset, None] = unset
    on_balance: Union[bool, Unset] = unset
    school_id: Union[int, Unset] = unset
    filename: Union[InMemoryUploadedFile, Unset, None] = unset
    cover: Union[InMemoryUploadedFile, Unset, None] = unset
    discipline_id: Union[int, Unset, None] = unset
    age_tag_id: Union[int, Unset, None] = unset
    status: Union[EntryStatus, Unset] = unset
    federal_book_id: Union[int, Unset, None] = unset

    class Config:
        title = 'Команда обновления библиотечного издания'
        arbitrary_types_allowed = True


class DeleteRegistryEntry(Command):
    id: int

    class Config:
        title = 'Команда удаления библиотечного издания'


class CreateRegistryExample(Command):
    lib_reg_entry_id: int
    invoice_number: str
    card_number: Optional[str]
    inflow_date: date
    max_date: Optional[str]
    edition: Optional[str]
    edition_place: str
    edition_year: int
    publishing_id: Optional[int]
    duration: str
    book_code: str
    price: Optional[Decimal]
    fin_source: Optional[FinSource]

    class Config:
        title = 'Команда создания экземпляра библиотечного издания'


class UpdateRegistryExample(Command):
    id: int
    invoice_number: Union[str, Unset] = unset
    card_number: Union[str, None, Unset] = unset
    inflow_date: Union[date, Unset] = unset
    max_date: Union[str, None, Unset] = unset
    edition: Union[str, None, Unset] = unset
    edition_place: Union[str, Unset] = unset
    edition_year: Union[int, Unset] = unset
    publishing_id: Union[int, None, Unset] = unset
    duration: Union[str, Unset] = unset
    book_code: Union[str, Unset] = unset
    price: Union[Decimal, None, Unset] = unset
    fin_source: Union[FinSource, None, Unset] = unset

    class Config:
        title = 'Команда обновления экземпляра библиотечного издания'


class DeleteRegistryExample(Command):
    id: int

    class Config:
        title = 'Команда удаления экземпляра библиотечного издания'


class CopyRegistryExample(Command):
    id: int
    count_for_copy: PositiveInt

    class Config:
        title = 'Команда копирования экземпляров библиотечного издания'
