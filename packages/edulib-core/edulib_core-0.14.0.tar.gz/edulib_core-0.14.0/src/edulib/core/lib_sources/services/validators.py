from typing import (
    TYPE_CHECKING,
)

from explicit.domain.model import (
    asdict,
)

from edulib.core.base.validation import (
    Validator,
    may_skip,
)
from edulib.core.lib_sources.domain.factories import (
    SourceDTO,
    factory,
)
from edulib.core.lib_sources.domain.model import (
    SourceNotFound,
)


if TYPE_CHECKING:
    from explicit.domain.factories import (
        DTOBase,
    )

    from edulib.core.lib_sources.domain.model import (
        Source,
    )
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )



class SourceValidator(Validator):
    """Валидатор источника поступления."""

    def __init__(self, data: 'DTOBase', uow: 'UnitOfWork') -> None:
        super().__init__(data, uow)

        self._source = None

    def validate_existence(self) -> 'SourceValidator':
        try:
            self._source = self._uow.sources.get_object_by_id(self._data.id)
        except SourceNotFound as exc:
            self._errors['id'].append(str(exc))
            self._skip_chain = True

        return self

    @may_skip
    def validate_name(self) -> 'SourceValidator':
        if 'name' in self._data.dict():
            name = self._data.name.strip()
            if name:
                source = self._create_source()
                if self._uow.sources.source_exists(source):
                    self._errors['name'].append(
                        f'Источник поступления с именем "{name}" уже существует'
                    )
            else:
                self._errors['name'].append('Наименование не может быть пустым')
        return self

    def _create_source(self) -> 'Source':
        if self._source:
            dto = SourceDTO(**asdict(self._source) | self._data.dict())
        else:
            dto = self._data

        return factory.create(dto)

    def validate_deletion_if_linked_entries_exist(self) -> 'SourceValidator':
        """Проверяет, можно ли удалить источник, исходя из наличия связанных записей LibRegistryEntry."""
        if obj := self._source:
            if self._uow.sources.has_linked_lib_registry_entry(obj):
                self._errors['id'].append(
                    f'Источник поступления "{obj.name}" связан с библиотечными изданиями и не может быть удален'
                )
        return self
