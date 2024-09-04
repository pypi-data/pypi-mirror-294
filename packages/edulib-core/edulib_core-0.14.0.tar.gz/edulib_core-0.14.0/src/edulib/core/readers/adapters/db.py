from collections.abc import (
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
from explicit.domain import (
    asdict,
)

from edulib.core.readers import (
    domain,
    models as db,
)


class ReaderRepository(AbstractRepository):
    def get_object_by_id(self, identifier: int) -> domain.Reader:
        try:
            db_instance = db.Reader.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as exc:
            raise domain.ReaderNotFound from exc

    def add(self, obj: domain.Reader) -> domain.Reader:
        assert isinstance(obj, domain.Reader)

        return self._to_db(obj)

    def update(self, obj: domain.Reader) -> domain.Reader:
        assert isinstance(obj, domain.Reader)

        return self._to_db(obj)

    def delete(self, obj: domain.Reader) -> None:
        assert isinstance(obj, domain.Reader)

        db.Reader.objects.filter(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[domain.Reader, None, None]:
        for entry in db.Reader.objects.iterator():
            yield self._to_domain(entry)

    def _to_domain(self, db_instance: db.Reader) -> domain.Reader:
        return domain.Reader(**model_to_dict(db_instance))

    def _to_db(self, modelinstance: domain.Reader) -> domain.Reader:
        assert isinstance(modelinstance, domain.Reader)

        db_instance, _ = db.Reader.objects.update_or_create(pk=modelinstance.id, defaults=asdict(modelinstance))
        modelinstance.id = db_instance.pk

        return modelinstance


readers = ReaderRepository()
