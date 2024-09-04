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

from edulib.core.lib_passport.documents import (
    domain,
    models as db,
)


class DocumentRepository(AbstractRepository):

    def get_object_by_id(self, identifier: int) -> domain.Document:
        try:
            db_instance = db.LibPassportDocuments.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as e:
            raise domain.DocumentNotFound() from e

    def add(self, obj: domain.Document) -> domain.Document:
        assert isinstance(obj, domain.Document)

        return self._to_db(obj)

    def update(self, obj: domain.Document) -> domain.Document:
        assert isinstance(obj, domain.Document)

        return self._to_db(obj)

    def delete(self, obj: domain.Document) -> None:
        assert isinstance(obj, domain.Document)
        db.LibPassportDocuments.objects.filter(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[domain.Document, None, None]:
        for document in db.LibPassportDocuments.objects.iterator():
            yield self._to_domain(document)

    def is_exists(self, document: domain.Document) -> bool:
        return (db.LibPassportDocuments.objects
                .exclude(pk=document.id)
                .filter(name__iexact=document.name)
                .exists()
                )

    def _to_db(self, modelinstance: domain.Document) -> domain.Document:
        assert isinstance(modelinstance, domain.Document)

        db_instance, _ = db.LibPassportDocuments.objects.update_or_create(
            pk=modelinstance.id,
            defaults=asdict(modelinstance),
        )
        modelinstance.id = db_instance.pk

        return modelinstance

    def _to_domain(self, dbinstance: db.LibPassportDocuments) -> domain.Document:
        return domain.Document(
            library_passport_id=dbinstance.library_passport_id,
            **model_to_dict(dbinstance)
        )


repository = DocumentRepository()
