from typing import (
    TYPE_CHECKING,
)

from edulib.core.base.tests.utils import (
    randint,
)

from ..domain import (
    SchoolDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from ..domain import (
        School,
    )


def get_school(uow: 'UnitOfWork', save: bool = True, **kwargs) -> 'School':
    params = {
        'id': randint(),
        'name': 'МБОУ г. Москвы "Средняя общеобразовательная школа № 13"',
        'short_name': 'СОШ 13',
        'status': True,
    } | kwargs

    school = factory.create(SchoolDTO(**params))

    if save:
        school = uow.schools.add(school)

    return school
