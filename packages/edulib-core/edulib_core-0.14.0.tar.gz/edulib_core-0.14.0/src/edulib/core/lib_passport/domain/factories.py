from typing import (
    Union,
)

from explicit.domain import (
    AbstractDomainFactory,
    DTOBase,
    Unset,
    unset,
)

from edulib.core.lib_passport.domain.model import (
    Passport,
    WorkMode,
)


class PassportDTO(DTOBase):

    id: Union[int, None, Unset] = unset
    school_id: Union[int, None, Unset] = unset
    name: Union[str, Unset] = unset
    date_found_month: Union[int, None, Unset] = unset
    date_found_year: Union[int, None, Unset] = unset
    library_chief_id: Union[int, None, Unset] = unset
    is_address_match: Union[bool, None, Unset] = unset
    is_telephone_match: Union[bool, None, Unset] = unset
    telephone: Union[int, None, Unset] = unset
    is_email_match: Union[bool, None, Unset] = unset
    email: Union[str, None, Unset] = unset
    academic_year_id: Union[int, None, Unset] = unset
    address_id: Union[int, None, Unset] = unset


class Factory(AbstractDomainFactory):

    def create(self, data: PassportDTO) -> Passport:
        return Passport(**data.dict())


factory = Factory()


class WorkModeDTO(DTOBase):

    id: Union[int, None, Unset] = unset
    lib_passport_id: Union[int, Unset] = unset
    schedule_mon_from: Union[str, None, Unset] = unset
    schedule_mon_to: Union[str, None, Unset] = unset
    schedule_tue_from: Union[str, None, Unset] = unset
    schedule_tue_to: Union[str, None, Unset] = unset
    schedule_wed_from: Union[str, None, Unset] = unset
    schedule_wed_to: Union[str, None, Unset] = unset
    schedule_thu_from: Union[str, None, Unset] = unset
    schedule_thu_to: Union[str, None, Unset] = unset
    schedule_fri_from: Union[str, None, Unset] = unset
    schedule_fri_to: Union[str, None, Unset] = unset
    schedule_sat_from: Union[str, None, Unset] = unset
    schedule_sat_to: Union[str, None, Unset] = unset
    schedule_sun_from: Union[str, None, Unset] = unset
    schedule_sun_to: Union[str, None, Unset] = unset


class WorkModeFactory(AbstractDomainFactory):

    def create(self, data: WorkModeDTO) -> WorkMode:
        return WorkMode(**data.dict())


work_mode_factory = WorkModeFactory()
