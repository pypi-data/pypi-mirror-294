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

from edulib.core.lib_passport.cleanup_days import (
    domain,
    models as db,
)


class CleanupDayRepository(AbstractRepository):

    def get_object_by_id(self, identifier: int) -> domain.CleanupDay:
        try:
            db_instance = db.CleanupDays.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as e:
            raise domain.CleanupDayNotFound() from e

    def add(self, obj: domain.CleanupDay) -> domain.CleanupDay:
        assert isinstance(obj, domain.CleanupDay)

        return self._to_db(obj)

    def update(self, obj: domain.CleanupDay) -> domain.CleanupDay:
        assert isinstance(obj, domain.CleanupDay)

        return self._to_db(obj)

    def delete(self, obj: domain.CleanupDay) -> None:
        assert isinstance(obj, domain.CleanupDay)
        db.CleanupDays.objects.filter(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[domain.CleanupDay, None, None]:
        for cleanup_day in db.CleanupDays.objects.iterator():
            yield self._to_domain(cleanup_day)

    def is_exists(self, cleanup_day: domain.CleanupDay) -> bool:
        return (db.CleanupDays.objects
                .exclude(pk=cleanup_day.id)
                .filter(cleanup_date=cleanup_day.cleanup_date, lib_passport_id=cleanup_day.lib_passport_id)
                .exists()
                )

    def _to_db(self, modelinstance: domain.CleanupDay) -> domain.CleanupDay:
        assert isinstance(modelinstance, domain.CleanupDay)

        db_instance, _ = db.CleanupDays.objects.update_or_create(
            pk=modelinstance.id,
            defaults=asdict(modelinstance),
        )

        modelinstance.id = db_instance.pk

        return modelinstance

    def _to_domain(self, dbinstance: db.CleanupDays) -> domain.CleanupDay:
        result = domain.CleanupDay(
            lib_passport_id=dbinstance.lib_passport_id,
            **model_to_dict(dbinstance),
        )
        return result


repository = CleanupDayRepository()
