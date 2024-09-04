from typing import (
    TYPE_CHECKING,
)

from edulib.core.academic_years.tests.utils import (
    get_academic_year,
)
from edulib.core.base.tests.utils import (
    generator,
    randint,
)
from edulib.core.classyears import (
    domain,
)
from edulib.core.employees.tests.utils import (
    get_employee,
)
from edulib.core.parallels.tests.utils import (
    get_parallel,
)
from edulib.core.schools.tests.utils import (
    get_school,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def get_class_year(uow: 'UnitOfWork', save: bool = True, **kwargs) -> domain.ClassYear:
    if not (school_id := kwargs.get('school_id')):
        school_id = get_school(uow).id

    if not (letter := kwargs.get('letter')):
        letter = chr(generator.randint(ord('А'), ord('Е')))

    if parallel_id := kwargs.get('parallel_id'):
        parallel = uow.parallels.get_object_by_id(parallel_id)
    else:
        parallel = get_parallel(uow)
        parallel_id = parallel.id

    if not (teacher_id := kwargs.get('teacher_id')):
        teacher_id = get_employee(uow, school_id=school_id).id

    if not (academic_year_id := kwargs.get('academic_year_id')):
        academic_year_id = get_academic_year(uow).id

    params = {
        'id': randint(),
        'school_id': school_id,
        'teacher_id': teacher_id,
        'parallel_id': parallel_id,
        'academic_year_id': academic_year_id,
        'letter': letter,
        'name': f'{parallel.title} {letter}',
    } | kwargs

    class_year = domain.factory.create(domain.ClassYearDTO(**params))

    if save:
        class_year = uow.classyears.add(class_year)

    return class_year
