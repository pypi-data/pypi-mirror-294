from django.test import (
    TransactionTestCase,
)

from edulib.core import (
    bus,
)
from edulib.core.employees.tests.utils import (
    get_employee,
)
from edulib.core.readers import (
    domain,
)
from edulib.core.readers.domain.model import (
    Reader,
)


class ReaderTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.uow = bus.get_uow()

        employee = get_employee(self.uow)
        self.initial_data = {
            'number': '12345',
            'teacher_id': employee.id,
            'role': domain.ReaderRole.TEACHER,
            'school_id': employee.school_id,
        }
        self.changed_data = {
            'number': '54321',
        }

    def test_update_reader(self) -> None:
        reader = self.uow.readers.add(Reader(**self.initial_data))

        changed_reader = bus.handle(domain.UpdateReader(id=reader.id, **self.changed_data))

        for field, value in (self.initial_data | self.changed_data).items():
            with self.subTest(field=field):
                result = getattr(changed_reader, field)
                self.assertEqual(result, value)
