from datetime import (
    date,
)
from typing import (
    TYPE_CHECKING,
)

from django.utils import (
    timezone,
)

from edulib.core.academic_years import (
    domain,
)
from edulib.core.base.tests.utils import (
    randint,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def get_academic_year(uow: 'UnitOfWork', save: bool = True, **kwargs) -> domain.AcademicYear:
    if not (year := kwargs.get('year')):
        now = timezone.now()
        year = now.year if now.month > 8 else now.year - 1

    date_begin = date(year, 9, 1)
    date_end = date(year + 1, 8, 31)

    params = {
        'id': randint(),
        'date_begin': date_begin,
        'date_end': date_end,
        'name': f'{date_begin.year}/{date_end.year}',
        'code': f'{date_begin.year % 100}/{date_end.year % 100}',
    } | kwargs

    academic_year = domain.factory.create(domain.AcademicYearDTO(**params))

    if save:
        academic_year = uow.academic_years.add(academic_year)

    return academic_year
