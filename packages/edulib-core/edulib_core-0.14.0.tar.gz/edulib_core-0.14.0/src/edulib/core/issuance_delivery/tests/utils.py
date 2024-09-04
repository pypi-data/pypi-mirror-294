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
)
from edulib.core.issuance_delivery import (
    domain,
)
from edulib.core.lib_registry.tests.utils import (
    get_registry_example,
)
from edulib.core.readers.tests.utils import (
    get_reader,
)
from edulib.core.schools.tests.utils import (
    get_school,
)


if TYPE_CHECKING:
    from edulib.core.unit_of_work import (
        UnitOfWork,
    )


def get_issuance_delivery(uow: 'UnitOfWork', save: bool = True, **kwargs) -> domain.IssuanceDelivery:
    if not (school_id := kwargs.get('school_id')):
        school_id = get_school(uow, save).id

    if not (reader_id := kwargs.get('reader_id')):
        reader_id = get_reader(uow, save, school_id=school_id).id

    if not (example_id := kwargs.get('example_id')):
        example_id = get_registry_example(uow, save, school_id=school_id).id

    if not (issuance_date := kwargs.get('issuance_date')):
        issuance_date = timezone.now() - timedelta(days=30)

    if not (extension_days_count := kwargs.get('extension_days_count')):
        extension_days_count = generator.randint(5, 15)

    params = {
        'issuance_date': issuance_date,
        'reader_id': reader_id,
        'example_id': example_id,
        'extension_days_count': extension_days_count,
    } | kwargs

    issuance_delivery = domain.issuance_delivery_factory.create(domain.IssuanceDeliveryDTO(**params))

    if save:
        issuance_delivery = uow.issuance_deliveries.add(issuance_delivery)

    return issuance_delivery
