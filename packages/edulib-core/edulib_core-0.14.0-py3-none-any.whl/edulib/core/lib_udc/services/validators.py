from typing import (
    Optional,
)

from explicit.domain import (
    asdict,
)

from edulib.core.base.validation import (
    Validator,
    may_skip,
)
from edulib.core.lib_udc.domain import (
    Udc,
    UdcDTO,
    UdcNotFound,
    factory,
)


class UdcValidator(Validator):
    """Валидатор раздела УДК."""

    def validate_existence(self) -> 'UdcValidator':
        if not self._get_udc(self._data.id, 'id'):
            self._skip_chain = True

        return self

    @may_skip
    def validate_parent(self) -> 'UdcValidator':
        if self._data.parent_id:
            self._get_udc(self._data.parent_id, 'parent_id')

        return self

    @may_skip
    def validate_code(self, *, is_update: bool = False) -> 'UdcValidator':
        if 'code' in self._data.dict():
            code = self._data.code.strip()
            if code:
                if is_update:
                    udc = self._get_udc(self._data.id, 'id')
                    dto = UdcDTO(**asdict(udc) | self._data.dict())
                else:
                    dto = self._data

                if self._uow.udc.is_exists(factory.create(dto)):
                    self._errors['code'].append('Такой раздел УДК уже существует')

        return self

    def _get_udc(self, identifier: int, error_name: str) -> Optional[Udc]:
        try:
            return self._uow.udc.get_object_by_id(identifier)
        except UdcNotFound as exc:
            self._errors[error_name].append(str(exc))
