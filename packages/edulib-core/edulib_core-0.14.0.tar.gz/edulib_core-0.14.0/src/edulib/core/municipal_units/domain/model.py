from pydantic import (
    Field,
)
from pydantic.dataclasses import (
    dataclass,
)


class MunicipalUnitNotFound(Exception):

    def __init__(self, *args):
        super().__init__('Муниципальная единица не найдена', *args)


@dataclass
class MunicipalUnit:
    """Муниципальная единица.

    Является проекцией сущностей внешних ИС.
    """

    id: int = Field(title='Глобальный идентификатор')
    name: str = Field(title='Наименование')
    constituent_entity: str = Field(title='Наименование субъекта РФ', max_length=200)
    oktmo: str = Field(title='ОКТМО', max_length=11)
