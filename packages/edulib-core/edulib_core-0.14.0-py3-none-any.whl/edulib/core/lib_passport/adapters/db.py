from typing import (
    Generator,
)

from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.forms import (
    model_to_dict,
)
from explicit.adapters.db import (
    AbstractRepository,
)
from explicit.domain.model import (
    asdict,
)

from edulib.core.lib_passport import (
    domain,
    models as db,
)


class PassportRepository(AbstractRepository):

    def get_object_by_id(self, identifier: int) -> domain.Passport:
        try:
            db_instance = db.LibPassport.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as e:
            raise domain.PassportNotFound() from e

    def add(self, obj: domain.Passport) -> domain.Passport:
        assert isinstance(obj, domain.Passport)

        return self._to_db(obj)

    def update(self, obj: domain.Passport) -> domain.Passport:
        assert isinstance(obj, domain.Passport)

        return self._to_db(obj)

    def delete(self, obj: domain.Passport) -> None:
        assert isinstance(obj, domain.Passport)
        db.LibPassport.objects.filter(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[domain.Passport, None, None]:
        for passport in db.LibPassport.objects.iterator():
            yield self._to_domain(passport)

    def is_exists(self, passport: domain.Passport) -> bool:
        return (db.LibPassport.objects
                .exclude(pk=passport.id)
                .filter(name__iexact=passport.name, school_id=passport.school_id)
                .exists()
                )

    def get_by_school_id(self, school_id: int) -> domain.Passport:
        try:
            return self._to_domain(
                db.LibPassport.objects.get(school_id=school_id)
            )
        except ObjectDoesNotExist as e:
            raise domain.PassportNotFound() from e

    def _to_db(self, modelinstance: domain.Passport) -> domain.Passport:
        assert isinstance(modelinstance, domain.Passport)

        db_instance, _ = db.LibPassport.objects.update_or_create(
            pk=modelinstance.id,
            school_id=modelinstance.school_id,
            library_chief_id=modelinstance.library_chief_id,
            academic_year_id=modelinstance.academic_year_id,
            address_id=modelinstance.address_id,
            defaults=asdict(modelinstance)
        )

        modelinstance.id = db_instance.pk

        return modelinstance

    def _to_domain(self, dbinstance: db.LibPassport) -> domain.Passport:
        result = domain.Passport(
            school_id=dbinstance.school_id,
            library_chief_id=dbinstance.library_chief_id,
            academic_year_id=dbinstance.academic_year_id,
            address_id=dbinstance.address_id,
            **model_to_dict(dbinstance, exclude=[
                'school',
                'library_chief',
                'academic_year',
                'address',
            ])
        )

        return result


passport_repository = PassportRepository()


class WorkModeRepository(AbstractRepository):

    def get_object_by_id(self, identifier: int) -> domain.WorkMode:
        try:
            db_instance = db.WorkMode.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as e:
            raise domain.WorkModeNotFound() from e

    def add(self, obj: domain.WorkMode) -> domain.WorkMode:
        assert isinstance(obj, domain.WorkMode)

        return self._to_db(obj)

    def update(self, obj: domain.WorkMode) -> domain.WorkMode:
        assert isinstance(obj, domain.WorkMode)

        return self._to_db(obj)

    def delete(self, obj: domain.WorkMode) -> None:
        assert isinstance(obj, domain.WorkMode)
        db.WorkMode.objects.filter(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[domain.WorkMode, None, None]:
        for work_mode in db.WorkMode.objects.iterator():
            yield self._to_domain(work_mode)

    def is_exists(self, work_mode: domain.WorkMode) -> bool:
        return (db.WorkMode.objects
                .exclude(pk=work_mode.id)
                .filter(lib_passport=work_mode.lib_passport_id)
                .exists()
                )

    def _to_db(self, modelinstance: domain.WorkMode) -> domain.WorkMode:
        assert isinstance(modelinstance, domain.WorkMode)

        db_instance, _ = db.WorkMode.objects.update_or_create(
            pk=modelinstance.id,
            defaults=asdict(modelinstance),
        )
        modelinstance.id = db_instance.pk

        return modelinstance

    def _to_domain(self, dbinstance: db.WorkMode) -> domain.WorkMode:
        return domain.WorkMode(
            lib_passport_id=dbinstance.lib_passport_id,
            **model_to_dict(dbinstance)
        )


work_mode_repository = WorkModeRepository()
