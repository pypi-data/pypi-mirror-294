from typing import (
    TYPE_CHECKING,
)

from edulib.core.base.tests.utils import (
    randint,
)
from edulib.core.parent_types.tests.utils import (
    get_parent_type,
)
from edulib.core.persons.tests.utils import (
    get_person,
)

from ..domain import (
    ParentDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from ..domain import (
        Parent,
    )


def get_parent(uow: 'UnitOfWork', save: bool = True, **kwargs) -> 'Parent':
    if not (parent_person_id := kwargs.get('parent_person_id')):
        parent_person_id = get_person(uow, save=save).id

    if not (child_person_id := kwargs.get('child_person_id')):
        child_person_id = get_person(uow, save=save).id

    if not (parent_type_id := kwargs.get('parent_type_id')):
        parent_type_id = get_parent_type(uow, save=save).id

    params = {
        'id': randint(),
        'parent_person_id': parent_person_id,
        'child_person_id': child_person_id,
        'parent_type_id': parent_type_id,
        'status': True,
    } | kwargs

    parent = factory.create(ParentDTO(**params))

    if save:
        parent = uow.parents.add(parent)

    return parent
