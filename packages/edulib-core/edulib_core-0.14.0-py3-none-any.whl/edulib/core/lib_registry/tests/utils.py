import secrets
from datetime import (
    timedelta,
)
from typing import (
    TYPE_CHECKING,
)

from django.utils import (
    timezone,
)

from edulib.core.base.tests.utils import (
    generator,
    randstr,
)
from edulib.core.directory.models import (
    Catalog,
)
from edulib.core.disciplines.tests.utils import (
    get_discipline,
)
from edulib.core.lib_authors.tests.utils import (
    get_author,
)
from edulib.core.lib_example_types.models import (
    LibraryExampleType,
)
from edulib.core.lib_registry import (
    domain,
)
from edulib.core.lib_registry.models import (
    LibMarkInformProduct,
)
from edulib.core.lib_udc.models import (
    LibraryUDC,
)
from edulib.core.schools.tests.utils import (
    get_school,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def get_registry_entry(uow: 'UnitOfWork', save: bool = True, **kwargs) -> domain.RegistryEntry:  # pylint: disable=too-many-locals
    if not (type_id := kwargs.get('type_id')):
        entry_type, _ = LibraryExampleType.objects.get_or_create(id=1, name='Учебник, учебная литература')
        type_id = entry_type.id

    if not (bbc_id := kwargs.get('bbc_id')):
        bbc, _ = Catalog.objects.get_or_create(id=103, code='86.7', name='Свободомыслие')
        bbc_id = bbc.id

    if not (udc_id := kwargs.get('udc_id')):
        udc, _ = LibraryUDC.objects.get_or_create(id=10, code='8', name='Языкознание')
        udc_id = udc.id

    if not (age_tag_id := kwargs.get('age_tag_id')):
        age_tag, _ = LibMarkInformProduct.objects.get_or_create(id=3, code='12+', name='для детей старше 12 лет')
        age_tag_id = age_tag.id

    if not (school_id := kwargs.get('school_id')):
        school_id = get_school(uow, save).id

    if not (author_id := kwargs.get('author_id')):
        author_id = get_author(uow, save).id

    if not (discipline_id := kwargs.get('discipline_id')):
        discipline_id = get_discipline(uow, save).id

    if not (title := kwargs.get('title')):
        title = secrets.choice((
            'Русский язык: 9-й класс: учебник',
            'Литература: 8-й класс: учебник: в 2 частях',
            'Английский язык: 8-й класс: учебник',
            'Китайский : второй иностранный язык : 8-й класс : учебник',
            'История. История России. XIX — начало XX века: 9-й класс: учебник',
        ))

    params = {
        'type_id': type_id,
        'bbc_id': bbc_id,
        'udc_id': udc_id,
        'age_tag_id': age_tag_id,
        'author_id': author_id,
        'school_id': school_id,
        'discipline_id': discipline_id,
        'title': title,
    } | kwargs

    registry_entry = domain.entry_factory.create(domain.RegistryEntryDTO(**params))

    if save:
        registry_entry = uow.registry_entries.add(registry_entry)

    return registry_entry


def get_registry_example(uow: 'UnitOfWork', save: bool = True, **kwargs) -> domain.RegistryExample:
    if not (school_id := kwargs.get('school_id')):
        school_id = get_school(uow, save).id

    if not (lib_reg_entry_id := kwargs.get('lib_reg_entry_id')):
        lib_reg_entry_id = get_registry_entry(uow, save, school_id=school_id).id

    if not (inflow_date := kwargs.get('inflow_date')):
        inflow_date = timezone.now() - timedelta(days=365)

    if not (edition_place := kwargs.get('edition_place')):
        edition_place = secrets.choice((
            'Москва',
            'Санкт-Петербург',
            'Новосибирск',
        ))

    if not (edition_year := kwargs.get('edition_year')):
        edition_year = generator.randrange(2000, timezone.now().year)

    if not (duration := kwargs.get('duration')):
        duration = generator.randrange(50, 500)

    if not (book_code := kwargs.get('book_code')):
        book_code = randstr(domain.RegistryExample.book_code.max_length)

    if not (max_date := kwargs.get('max_date')):
        max_date = generator.randint(10, 20)

    params = {
        'lib_reg_entry_id': lib_reg_entry_id,
        'inflow_date': inflow_date,
        'edition_place': edition_place,
        'edition_year': edition_year,
        'duration': duration,
        'book_code': book_code,
        'max_date': max_date,
    } | kwargs

    registry_example = domain.example_factory.create(domain.RegistryExampleDTO(**params))

    if save:
        registry_example = uow.registry_examples.add(registry_example)

    return registry_example
