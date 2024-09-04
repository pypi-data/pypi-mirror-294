from typing import (
    TYPE_CHECKING,
)

from edulib.core.base.tests.utils import (
    generator,
    randint,
)
from edulib.core.parallels import (
    domain,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def get_parallel(uow: 'UnitOfWork', save: bool = True, **kwargs) -> domain.Parallel:
    if not (title := kwargs.get('title')):
        title = generator.randint(1, 11)

    params = {
        'id': randint(),
        'title': title,
        'system_object_id': generator.randint(1, 2**31 - 1),
        'object_status': True,
    } | kwargs

    parallel = domain.factory.create(domain.ParallelDTO(**params))

    if save:
        parallel = uow.parallels.add(parallel)

    return parallel
