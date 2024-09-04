from typing import (
    Optional,
)

from edulib.core.base.validation import (
    Validator,
    may_skip,
)
from edulib.core.lib_passport.cleanup_days.domain import (
    CleanupDay,
    CleanupDayNotFound,
    factory,
)


class CleanupDayValidator(Validator):

    def validate_existence(self) -> 'CleanupDayValidator':
        if not self._get_cleanup_day(self._data.id, 'id'):
            self._skip_chain = True

        return self

    @may_skip
    def validate_cleanup_date(self) -> 'CleanupDayValidator':
        if self._uow.cleanup_days.is_exists(factory.create(self._data)):
            self._errors['cleanup_date'].append('Санитарный день уже существует')

        return self

    def _get_cleanup_day(self, identifier: int, error_name: str) -> Optional[CleanupDay]:
        try:
            return self._uow.cleanup_days.get_object_by_id(identifier)
        except CleanupDayNotFound as exc:
            self._errors[error_name].append(str(exc))
