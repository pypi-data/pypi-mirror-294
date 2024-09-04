from datetime import (
    date,
)
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
)

from explicit.contrib.domain.model import (
    identifier,
)
from pydantic import (
    Field,
    validator,
)
from pydantic.dataclasses import (
    dataclass,
)


if TYPE_CHECKING:
    from pydantic.fields import (
        ModelField,
    )


class IssuanceDeliveryNotFound(Exception):
    """Возбуждается, когда выдача экземпляра не может быть определена."""

    def __init__(self, *args):
        super().__init__('Выдача экземпляра не найдена', *args)


@dataclass(config={'validate_assignment': True})
class IssuanceDelivery:
    id: Optional[int] = identifier()
    issuance_date: date = Field(
        title='Дата выдачи экземпляра издания',
    )
    fact_delivery_date: Optional[date] = Field(
        title='Фактическая дата сдачи экземпляра',
    )
    reader_id: int = Field(
        title='Читатель, получивший экземпляр',
    )
    example_id: int = Field(
        title='Экземпляр издания',
    )
    special_notes: Optional[str] = Field(
        title='Комментарий',
        max_length=300,
    )
    extension_days_count: Optional[int] = Field(
        title='Количество дней на продление выдачи',
        gt=0,
    )

    @validator('fact_delivery_date')
    def not_earlier_issuance_date(  # pylint: disable=no-self-argument
        cls,
        value: Optional[date],
        field: 'ModelField',
        values: dict[str, Any],
    ) -> Optional[date]:
        if value is not None and value < values['issuance_date']:
            raise ValueError(f'{field.field_info.title} не может быть раньше даты выдачи экземпляра издания')

        return value
