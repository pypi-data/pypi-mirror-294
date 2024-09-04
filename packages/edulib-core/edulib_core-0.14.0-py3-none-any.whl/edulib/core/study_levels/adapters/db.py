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
    def _base_qs(self) -> 'QuerySet[db.StudyLevel]':
        return db.StudyLevel.objects.all()

    @property
    def _base_qs_with_deleted(self) -> 'QuerySet[db.StudyLevel]':
        return db.StudyLevel.objects.all()

    def get_all_objects(self) -> Generator[domain.StudyLevel, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def add(self, study_level: domain.StudyLevel) -> domain.StudyLevel:
        assert isinstance(study_level, domain.StudyLevel)

        return self._to_db(study_level)

    def update(self, study_level: domain.StudyLevel) -> domain.StudyLevel:
        assert isinstance(study_level, domain.StudyLevel)

        return self._to_db(study_level)

    def delete(self, study_level: domain.StudyLevel):
        self._base_qs.filter(id=study_level.id).delete()

    def _to_db(self, study_level: domain.StudyLevel) -> domain.StudyLevel:
        assert isinstance(study_level, domain.StudyLevel)

        db_instance, _ = self._base_qs.update_or_create(
            pk=study_level.id, defaults=asdict(study_level)
        )
        study_level.id = db_instance.pk
        assert study_level.id is not None

        return study_level

    def _to_domain(self, dbinstance: 'db.StudyLevel') -> domain.StudyLevel:
        study_level = domain.StudyLevel(**model_to_dict(dbinstance))

        return study_level

    def get_object_by_id(self, identifier: int) -> domain.StudyLevel:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.StudyLevelNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.StudyLevel, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())


repository = Repository()
