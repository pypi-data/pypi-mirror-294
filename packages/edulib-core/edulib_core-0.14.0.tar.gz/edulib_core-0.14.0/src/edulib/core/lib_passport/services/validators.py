from typing import (
    Optional,
)

from explicit.domain import (
    asdict,
)

from edulib.core.academic_years.domain import (
    AcademicYearNotFound,
)
from edulib.core.address.domain import (
    AddressNotFound,
)
from edulib.core.base.validation import (
    Validator,
    may_skip,
)
from edulib.core.employees.domain import (
    EmployeeNotFound,
)
from edulib.core.lib_passport.domain import (
    Passport,
    PassportDTO,
    PassportNotFound,
    WorkMode,
    WorkModeNotFound,
    factory,
    work_mode_factory,
)
from edulib.core.schools.domain import (
    SchoolNotFound,
)


class PassportValidator(Validator):
    """Валидатор паспорта библиотеки."""

    def validate_existence(self) -> 'PassportValidator':
        if not self._get_passport(self._data.id, 'id'):
            self._skip_chain = True

        return self

    @may_skip
    def validate_name(self, *, is_update: bool = False) -> 'PassportValidator':
        if 'name' in self._data.dict():
            name = self._data.name.strip()
            if name:
                if is_update:
                    passport = self._get_passport(self._data.id, 'id')
                    dto = PassportDTO(**asdict(passport) | self._data.dict())
                else:
                    dto = self._data

                if self._uow.passports.is_exists(factory.create(dto)):
                    self._errors['name'].append('Такой паспорт библиотеки уже существует')

        return self

    @may_skip
    def validate_school(self) -> 'PassportValidator':
        if 'school_id' in self._data.dict() and self._data.school_id is not None:
            try:
                self._uow.schools.get_object_by_id(self._data.school_id)
            except SchoolNotFound as exc:
                self._errors['school_id'].append(str(exc))

        return self

    @may_skip
    def validate_address(self) -> 'PassportValidator':
        if 'address_id' in self._data.dict() and self._data.address_id is not None:
            try:
                self._uow.addresses.get_object_by_id(self._data.address_id)
            except AddressNotFound as exc:
                self._errors['address_id'].append(str(exc))

        return self

    @may_skip
    def validate_academic_year(self) -> 'PassportValidator':
        if 'academic_year_id' in self._data.dict() and self._data.academic_year_id is not None:
            try:
                self._uow.academic_years.get_object_by_id(self._data.academic_year_id)
            except AcademicYearNotFound as exc:
                self._errors['academic_year_id'].append(str(exc))

        return self

    @may_skip
    def validate_library_chief(self) -> 'PassportValidator':
        if 'library_chief_id' in self._data.dict() and self._data.library_chief_id is not None:
            try:
                self._uow.employees.get_object_by_id(self._data.library_chief_id)
            except EmployeeNotFound as exc:
                self._errors['library_chief_id'].append(str(exc))

        return self

    def _get_passport(self, identifier: int, error_name: str) -> Optional[Passport]:
        try:
            return self._uow.passports.get_object_by_id(identifier)
        except PassportNotFound as exc:
            self._errors[error_name].append(str(exc))


class WorkModeValidator(Validator):

    def validate_existence(self) -> 'WorkModeValidator':
        if not self._get_work_mode(self._data.id, 'id'):
            self._skip_chain = True

        return self

    @may_skip
    def validate_lib_passport(self) -> 'WorkModeValidator':
        if 'lib_passport_id' in self._data.dict() and self._data.lib_passport_id is not None:
            try:
                self._uow.passports.get_object_by_id(self._data.lib_passport_id)
            except PassportNotFound as exc:
                self._errors['lib_passport_id'].append(str(exc))
            if self._uow.work_modes.is_exists(work_mode_factory.create(self._data)):
                self._errors['lib_passport_id'].append('Режим работы уже существует')

        return self

    def _get_work_mode(self, identifier: int, error_name: str) -> Optional[WorkMode]:
        try:
            return self._uow.work_modes.get_object_by_id(identifier)
        except WorkModeNotFound as exc:
            self._errors[error_name].append(str(exc))
