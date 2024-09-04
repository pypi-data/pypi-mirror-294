from typing import (
    TYPE_CHECKING,
    Generator,
    Iterable,
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

from .. import (
    domain,
    models as db,
)


if TYPE_CHECKING:
    from dataclasses import (
        dataclass,
    )

    from django.db.models.query import (
        QuerySet,
    )


class Repository(AbstractRepository):

    @property
    def _base_qs(self) -> 'QuerySet[db.ParentType]':
        return db.ParentType.objects.all()

    @property
    def _base_qs_with_deleted(self) -> 'QuerySet[db.ParentType]':
        return db.ParentType.objects.all()

    def get_all_objects(self) -> Generator[domain.ParentType, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def add(self, parent_type: domain.ParentType) -> domain.ParentType:
        assert isinstance(parent_type, domain.ParentType)

        return self._to_db(parent_type)

    def update(self, parent_type: domain.ParentType) -> domain.ParentType:
        assert isinstance(parent_type, domain.ParentType)

        return self._to_db(parent_type)

    def delete(self, parent_type: domain.ParentType):
        self._base_qs.filter(id=parent_type.id).delete()

    def _to_db(self, parent_type: domain.ParentType) -> domain.ParentType:
        assert isinstance(parent_type, domain.ParentType)

        db_instance, _ = self._base_qs.update_or_create(
            pk=parent_type.id, defaults=asdict(parent_type)
        )
        parent_type.id = db_instance.pk
        assert parent_type.id is not None

        return parent_type

    def _to_domain(self, dbinstance: 'db.ParentType') -> domain.ParentType:
        parent_type = domain.ParentType(**model_to_dict(dbinstance))

        return parent_type

    def get_object_by_id(self, identifier: int) -> domain.ParentType:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.ParentTypeNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.ParentType, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())


repository = Repository()
