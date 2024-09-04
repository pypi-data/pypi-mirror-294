from typing import (
    TYPE_CHECKING,
)

from django.utils import (
    timezone,
)

from edulib.core.base.tests.utils import (
    randint,
    randstr,
)
from edulib.core.employees.tests.utils import (
    get_employee,
)
from edulib.core.readers import (
    domain,
)
from edulib.core.schools.tests.utils import (
    get_school,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def get_reader(uow: 'UnitOfWork', save: bool = True, **kwargs) -> domain.Reader:
    if not (school_id := kwargs.get('school_id')):
        school_id = get_school(uow, save=save).id

    if not (teacher_id := kwargs.get('teacher_id')):
        teacher_id = get_employee(uow, save=save, school_id=school_id).id

    params = {
        'id': randint(),
        'teacher_id': teacher_id,
        'number': randstr(domain.Reader.number.max_length),
        'year': timezone.now().year,
        'role': domain.ReaderRole.TEACHER,
    } | kwargs

    reader = domain.reader_factory.create(domain.ReaderDTO(**params))

    if save:
        reader = uow.readers.add(reader)

    return reader
