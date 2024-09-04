from typing import (
    TYPE_CHECKING,
)

from ..domain import (
    InstitutionTypeDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )

    from ..domain import (
        InstitutionType,
    )


def get_institution_type(uow: 'UnitOfWork', save: bool = True, **kwargs) -> 'InstitutionType':
    params = {
        'id': 3,
        'name': 'Общеобразовательная организация',
    } | kwargs

    institution_type = factory.create(InstitutionTypeDTO(**params))

    if save:
        institution_type = uow.institution_types.add(institution_type)

    return institution_type
