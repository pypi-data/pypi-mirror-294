from datetime import (
    date,
)
from decimal import (
    Decimal,
)
from typing import (
    Union,
)

from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
)
from explicit.domain import (
    Unset,
    unset,
)
from explicit.domain.factories import (
    AbstractDomainFactory,
    DTOBase,
)

from .model import (
    EntryStatus,
    FinSource,
    RegistryEntry,
    RegistryExample,
)


class RegistryEntryDTO(DTOBase):
    id: Union[int, None, Unset] = unset
    type_id: Union[int, Unset] = unset
    title: Union[str, None, Unset] = unset
    author_id: Union[int, None, Unset] = unset
    parallel_ids: Union[list[int], None, Unset] = unset
    bbc_id: Union[int, None, Unset] = unset
    udc_id: Union[int, None, Unset] = unset
    tags: Union[str, None, Unset] = unset
    source_id: Union[int, None, Unset] = unset
    short_info: Union[str, None, Unset] = unset
    on_balance: Union[bool, Unset] = unset
    school_id: Union[int, Unset] = unset
    filename: Union[InMemoryUploadedFile, None, Unset] = unset
    cover: Union[InMemoryUploadedFile, None, Unset] = unset
    discipline_id: Union[int, None, Unset] = unset
    author_sign: Union[str, None, Unset] = unset
    age_tag_id: Union[int, None, Unset] = unset
    status: Union[EntryStatus, Unset] = unset
    federal_book_id: Union[int, None, Unset] = unset

    class Config:
        arbitrary_types_allowed = True


class RegistryEntryFactory(AbstractDomainFactory):
    def create(self, data: RegistryEntryDTO) -> RegistryEntry:
        return RegistryEntry(**data.dict())


entry_factory = RegistryEntryFactory()


class RegistryExampleDTO(DTOBase):
    id: Union[int, None, Unset] = unset
    lib_reg_entry_id: Union[int, Unset] = unset
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
    count_for_copy: Union[int, Unset] = unset


class RegistryExampleFactory(AbstractDomainFactory):
    def create(self, data: RegistryExampleDTO) -> RegistryExample:
        return RegistryExample(**data.dict())


example_factory = RegistryExampleFactory()
