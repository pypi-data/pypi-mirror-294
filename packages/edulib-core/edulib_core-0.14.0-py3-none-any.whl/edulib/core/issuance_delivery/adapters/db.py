from collections.abc import (
    Generator,
)
from datetime import (
    date,
)
from typing import (
    TYPE_CHECKING,
)

from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.db.models import (
    Q,
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

from edulib.core.issuance_delivery import (
    domain,
    models as db,
)


if TYPE_CHECKING:
    from django.db.models.query import (
        QuerySet,
    )


class IssuanceDeliveryRepository(AbstractRepository):
    def get_object_by_id(self, identifier: int) -> domain.IssuanceDelivery:
        try:
            db_instance = db.IssuanceDelivery.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as exc:
            raise domain.IssuanceDeliveryNotFound from exc

    def add(self, obj: domain.IssuanceDelivery) -> domain.IssuanceDelivery:
        assert isinstance(obj, domain.IssuanceDelivery)

        return self._to_db(obj)

    def update(self, obj: domain.IssuanceDelivery) -> domain.IssuanceDelivery:
        assert isinstance(obj, domain.IssuanceDelivery)

        return self._to_db(obj)

    def delete(self, obj: domain.IssuanceDelivery) -> None:
        assert isinstance(obj, domain.IssuanceDelivery)

        db.IssuanceDelivery.objects.filter(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[domain.IssuanceDelivery, None, None]:
        for entry in db.IssuanceDelivery.objects.iterator():
            yield self._to_domain(entry)

    def _to_domain(self, db_instance: db.IssuanceDelivery) -> domain.IssuanceDelivery:
        return domain.IssuanceDelivery(
            reader_id=db_instance.reader_id,
            example_id=db_instance.example_id,
            **model_to_dict(db_instance, exclude=('reader', 'example')),
        )

    def _to_db(self, modelinstance: domain.IssuanceDelivery) -> domain.IssuanceDelivery:
        assert isinstance(modelinstance, domain.IssuanceDelivery)

        db_instance, _ = db.IssuanceDelivery.objects.update_or_create(
            pk=modelinstance.id,
            defaults=asdict(modelinstance),
        )
        modelinstance.id = db_instance.pk

        return modelinstance

    def is_issued(self, issuance_delivery: domain.IssuanceDelivery) -> bool:
        assert isinstance(issuance_delivery, domain.IssuanceDelivery)

        return self._get_issued().filter(
            example_id=issuance_delivery.example_id,
        ).exists()

    def _get_issued(self) -> 'QuerySet':
        """Экземпляры, находящиеся "на руках"."""
        return db.IssuanceDelivery.objects.filter(
            Q(Q(fact_delivery_date__isnull=True) | Q(fact_delivery_date__gt=date.today()))
        )


issuance_deliveries = IssuanceDeliveryRepository()
