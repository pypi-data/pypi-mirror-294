from datetime import (
    date,
)
from typing import (
    TYPE_CHECKING,
)
from uuid import (
    uuid4,
)

from dateutil.relativedelta import (
    relativedelta,
)

from edulib.core.genders.tests.utils import (
    get_gender,
)

from ..domain import (
    Person,
    PersonDTO,
    factory,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def get_person(uow: 'UnitOfWork', save: bool = True, **kwargs) -> Person:
    if not (gender_id := kwargs.get('gender_id')):
        gender_id = get_gender(uow).id

    params = {
        'id': str(uuid4()),
        'surname': 'Иванов',
        'firstname': 'Иван',
        'patronymic': 'Иванович',
        'date_of_birth': date.today() - relativedelta(years=25),
        'gender_id': gender_id,
    } | kwargs

    person = factory.create(PersonDTO(**params))

    if save:
        person = uow.persons.add(person)

    return person
