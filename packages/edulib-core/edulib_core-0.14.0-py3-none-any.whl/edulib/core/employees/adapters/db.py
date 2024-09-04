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
    from django.db.models.query import (
        QuerySet,
    )


class Repository(AbstractRepository):

    @property
    def _base_qs(self) -> 'QuerySet[db.Employee]':
        return db.Employee.objects.all()

    @property
    def _base_qs_with_deleted(self) -> 'QuerySet[db.Employee]':
        return db.Employee.objects.all()

    def get_all_objects(self) -> Generator[domain.Employee, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.iterator())

    def add(self, employee: domain.Employee) -> domain.Employee:
        assert isinstance(employee, domain.Employee)

        return self._to_db(employee)

    def update(self, employee: domain.Employee) -> domain.Employee:
        assert isinstance(employee, domain.Employee)

        return self._to_db(employee)

    def delete(self, employee: domain.Employee):
        self._base_qs.filter(id=employee.id).delete()

    def _to_db(self, employee: domain.Employee) -> domain.Employee:
        assert isinstance(employee, domain.Employee)

        db_instance, _ = self._base_qs.update_or_create(
            pk=employee.id, defaults=asdict(employee)
        )
        employee.id = db_instance.pk
        assert employee.id is not None

        return employee

    def _to_domain(self, dbinstance: 'db.Employee') -> domain.Employee:
        employee = domain.Employee(
            person_id=dbinstance.person_id,
            **model_to_dict(dbinstance, exclude=['person']),
        )

        return employee

    def get_object_by_id(self, identifier: int) -> domain.Employee:
        try:
            return self._to_domain(self._base_qs.get(pk=identifier))
        except ObjectDoesNotExist as e:
            raise domain.EmployeeNotFound() from e

    def get_objects_by_ids(self, identifiers: Iterable[int]) -> Generator[domain.Employee, None, None]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(id__in=identifiers).iterator())

    def get_by_person_id(self, person_id: int) -> Iterable[domain.Employee]:
        yield from (self._to_domain(dbinstance) for dbinstance in self._base_qs.filter(person_id=person_id).iterator())


repository = Repository()
