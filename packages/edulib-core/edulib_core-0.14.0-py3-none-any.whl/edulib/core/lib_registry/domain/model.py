from datetime import (
    date,
)
from decimal import (
    Decimal,
)
from typing import (
    Any,
    Optional,
)

from explicit.contrib.domain.model import (
    identifier,
)
from pydantic import (
    Field,
)
from pydantic.dataclasses import (
    dataclass,
)

from edulib.core.utils.enums import (
    NamedIntEnum,
)


class InfoProductMarkNotFound(Exception):
    """Возбуждается, когда знак информационной продукции не может быть определен."""

    def __init__(self, *args):
        super().__init__('Знак информационной продукции не найден', *args)


class RegistryEntryNotFound(Exception):
    """Возбуждается, когда библиотечное издание не может быть определено."""

    def __init__(self, *args) -> None:
        super().__init__('Библиотечное издание не найдено', *args)


class RegistryExampleNotFound(Exception):
    """Возбуждается, когда экземпляр библиотечного издания не может быть определен."""

    def __init__(self, *args) -> None:
        super().__init__('Экземпляр библиотечного издания не найден', *args)


@dataclass
class InfoProductMark:
    id: Optional[int] = identifier()
    code: str = Field(
        title='Код',
        max_length=20,
    )
    name: str = Field(
        title='Наименование',
        max_length=200,
    )


class EntryStatus(NamedIntEnum):
    """Статус издания."""

    CURRENT = 1, 'Действующие'
    DISCARDED = 2, 'Списанные'


class FinSource(NamedIntEnum):
    """Источник финансирования."""

    FEDERAL = 0, 'Федеральный бюджет'
    REGIONAL = 1, 'Региональный бюджет'
    MUNICIPAL = 2, 'Муниципальный бюджет'
    OWN = 3, 'Средства организации'
    SPONSOR = 4, 'Средства спонсоров'


@dataclass
class RegistryEntry:
    """Библиотечное издание."""

    id: Optional[int] = identifier()
    type_id: int = Field(
        title='Тип',
    )
    title: Optional[str] = Field(
        title='Наименование',
        max_length=350,
    )
    author_id: Optional[int] = Field(
        title='Автор',
    )
    parallel_ids: Optional[list[int]] = Field(
        title='Параллели',
    )
    bbc_id: Optional[int] = Field(
        title='Раздел ББК',
    )
    udc_id: Optional[int] = Field(
        title='Раздел УДК',
    )
    take_from_fund: bool = Field(
        title='Получено из фонда',
        default=False,
    )
    tags: Optional[str] = Field(
        title='Ключевые слова',
        max_length=350,
    )
    source_id: Optional[int] = Field(
        title='Источник поступления',
    )
    short_info: Optional[str] = Field(
        title='Краткое описание',
        max_length=1000,
    )
    school_id: int = Field(
        title='Организация',
    )
    on_balance: bool = Field(
        title='Принято на баланс',
        default=False,
    )
    all_in_fund: bool = Field(
        title='Издание со всеми экземплярами переданы в фонд',
        default=False,
    )
    filename: Any = Field(
        title='Файл',
    )
    cover: Any = Field(
        title='Обложка',
    )
    discipline_id: Optional[int] = Field(
        title='Предмет',
    )
    author_sign: Optional[str] = Field(
        title='Авторский знак',
        max_length=5,
        default='',
    )
    age_tag_id: Optional[int] = Field(
        title='Знак информационной продукции',
    )
    status: EntryStatus = Field(
        title='Статус',
        default=EntryStatus.CURRENT,
    )
    federal_book_id: Optional[int] = Field(
        title='Учебник федерального перечня',
    )


@dataclass
class RegistryExample:
    """Экземпляр библиотечного издания."""

    id: Optional[int] = identifier()
    lib_reg_entry_id: int = Field(
        title='Библиотечное издание',
    )
    invoice_number: str = Field(
        default='',
        title='Номер накладной',
        max_length=255,
    )
    card_number: Optional[str] = Field(
        title='Номер карточки учёта',
        max_length=20,
    )
    inflow_date: date = Field(
        title='Дата поступления',
    )
    max_date: Optional[str] = Field(
        title='Максимальный срок выдачи',
        max_length=5,
    )
    edition: Optional[str] = Field(
        title='Издание',
        max_length=50,
    )
    edition_place: str = Field(
        title='Место издания',
        max_length=50,
    )
    edition_year: int = Field(
        title='Год издания',
    )
    publishing_id: Optional[int] = Field(
        title='Издательство',
    )
    duration: str = Field(
        title='Количество страниц / длительность',
        max_length=10,
    )
    book_code: str = Field(
        title='Шифр',
        max_length=22,
    )
    price: Optional[Decimal] = Field(
        title='Стоимость',
    )
    fin_source: Optional[FinSource] = Field(
        title='Источник финансирования',
    )
