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
    def _base_qs(self) -> 'QuerySet[db.Discipline]':
        return db.Discipline.objects.all()

    @property
    def _base_qs_with_deleted(self) -> 'QuerySet[db.Discipline]':
        return db.Discipline.objects.all()

    def get_all_objects(self) -> Generator[domain.Discipline, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def add(self, discipline: domain.Discipline) -> domain.Discipline:
        assert isinstance(discipline, domain.Discipline)

        return self._to_db(discipline)

    def update(self, discipline: domain.Discipline) -> domain.Discipline:
        assert isinstance(discipline, domain.Discipline)

        return self._to_db(discipline)

    def delete(self, discipline: domain.Discipline):
        self._base_qs.filter(id=discipline.id).delete()

    def _to_db(self, discipline: domain.Discipline) -> domain.Discipline:
        assert isinstance(discipline, domain.Discipline)

        db_instance, _ = self._base_qs.update_or_create(
            pk=discipline.id, defaults=asdict(discipline)
        )
        discipline.id = db_instance.pk
        assert discipline.id is not None

        return discipline

    def _to_domain(self, dbinstance: 'db.Discipline') -> domain.Discipline:
        discipline = domain.Discipline(**model_to_dict(dbinstance))

        return discipline

    def get_object_by_id(self, identifier: int) -> domain.Discipline:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.DisciplineNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.Discipline, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())


repository = Repository()
