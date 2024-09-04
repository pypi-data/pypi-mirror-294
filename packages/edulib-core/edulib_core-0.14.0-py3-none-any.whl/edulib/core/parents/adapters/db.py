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
    def _base_qs(self) -> 'QuerySet[db.Parent]':
        return db.Parent.objects.all()

    def get_all_objects(self) -> Generator[domain.Parent, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def add(self, parent: domain.Parent) -> domain.Parent:
        assert isinstance(parent, domain.Parent)

        return self._to_db(parent)

    def update(self, parent: domain.Parent) -> domain.Parent:
        assert isinstance(parent, domain.Parent)

        return self._to_db(parent)

    def delete(self, parent: domain.Parent):
        self._base_qs.filter(id=parent.id).delete()

    def _to_db(self, parent: domain.Parent) -> domain.Parent:
        assert isinstance(parent, domain.Parent)

        db_instance, _ = self._base_qs.update_or_create(
            pk=parent.id, defaults=asdict(parent)
        )
        parent.id = db_instance.pk
        assert parent.id is not None

        return parent

    def _to_domain(self, dbinstance: 'db.Parent') -> domain.Parent:
        return domain.Parent(
            **model_to_dict(dbinstance) | {
                attname: getattr(dbinstance, attname)
                for attname in ('parent_person_id', 'child_person_id', 'parent_type_id')
            }

        )

    def get_object_by_id(self, identifier: int) -> domain.Parent:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.ParentNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.Parent, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())


repository = Repository()
