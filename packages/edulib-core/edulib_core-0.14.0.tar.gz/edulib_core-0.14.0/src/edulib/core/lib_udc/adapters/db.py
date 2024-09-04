from dataclasses import (
    asdict,
)
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

from edulib.core.lib_udc import (
    domain,
    models as db,
)


class Repository(AbstractRepository):

    def get_object_by_id(self, identifier: int) -> domain.Udc:
        """Получает объект по идентификатору."""
        try:
            db_instance = db.LibraryUDC.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as exc:
            raise domain.UdcNotFound from exc

    def add(self, obj: domain.Udc) -> domain.Udc:
        assert isinstance(obj, domain.Udc)

        return self._to_db(obj)

    def update(self, obj: domain.Udc) -> domain.Udc:
        assert isinstance(obj, domain.Udc)

        return self._to_db(obj)

    def delete(self, obj: domain.Udc) -> None:
        assert isinstance(obj, domain.Udc)
        db.LibraryUDC.objects.filter(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[domain.Udc, None, None]:
        for udc in db.LibraryUDC.objects.iterator():
            yield self._to_domain(udc)

    def is_exists(self, udc: domain.Udc) -> bool:
        """Проверяет существует ли раздел УДК с указанным кодом."""
        return db.LibraryUDC.objects.exclude(pk=udc.id).filter(code__iexact=udc.code).exists()

    def _to_db(self, modelinstance: domain.Udc) -> domain.Udc:
        assert isinstance(modelinstance, domain.Udc)

        db_instance, _ = db.LibraryUDC.objects.update_or_create(
            pk=modelinstance.id,
            defaults=asdict(modelinstance),
        )
        modelinstance.id = db_instance.pk

        return modelinstance

    def _to_domain(self, dbinstance: db.LibraryUDC) -> domain.Udc:
        return domain.Udc(
            parent_id=dbinstance.parent_id,
            **model_to_dict(dbinstance, exclude=['parent']),
        )


repository = Repository()
