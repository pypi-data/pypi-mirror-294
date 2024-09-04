from collections.abc import (
    Mapping,
)
from typing import (
    TYPE_CHECKING,
)

from explicit.domain.validation.exceptions import (
    init_messages_dict,
)


if TYPE_CHECKING:
    from explicit.adapters.db import (
        AbstractRepository,
    )
    from explicit.domain import (
        DTOBase,
    )

    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def may_skip(func):
    """Пропускает шаг валидации, если установлен флаг."""

    def wrapper(self, *args, **kwargs):
        if self._skip_chain:  # pylint: disable=protected-access
            return self

        return func(self, *args, **kwargs)

    return wrapper


class Validator:
    """Базовый класс валидатора.

    Представляет собой цепочку валидации данных, оканчивающуюся вызовом метода get_errors.
    """

    def __init__(self, data: 'DTOBase', uow: 'UnitOfWork') -> None:
        self._data = data
        self._uow = uow

        self._errors = init_messages_dict()
        self._skip_chain = False

    def get_errors(self) -> Mapping[str, list[str]]:
        """Возвращает ошибки валидации."""
        return self._errors

    def _validate_relation(
        self,
        field: str,
        repository: 'AbstractRepository',
        exception: type[Exception],
        *,
        skip_chain: bool = False,
    ) -> 'Validator':
        if (value := self._data.dict().get(field)) is not None:
            try:
                repository.get_object_by_id(value)
            except exception as exc:
                self._errors[field].append(str(exc))
                if skip_chain:
                    self._skip_chain = True

        return self
