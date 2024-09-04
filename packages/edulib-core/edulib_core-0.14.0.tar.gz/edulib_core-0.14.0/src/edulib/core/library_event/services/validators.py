from edulib.core.base.validation import (
    Validator,
    may_skip,
)
from edulib.core.lib_passport.domain.model import (
    PassportNotFound,
)
from edulib.core.library_event.domain.model import (
    EventNotFound,
)


class EventValidator(Validator):
    """Валидатор плана работы библиотеки."""

    def validate_existence(self) -> 'EventValidator':
        try:
            self._uow.events.get_object_by_id(self._data.id)
        except EventNotFound as exc:
            self._errors['id'].append(str(exc))
            self._skip_chain = True

        return self

    @may_skip
    def validate_passport(self) -> 'EventValidator':
        return self._validate_relation('library_id', self._uow.passports, PassportNotFound)
