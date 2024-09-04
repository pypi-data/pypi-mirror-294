from datetime import (
    date,
)

from django.test.testcases import (
    TransactionTestCase,
)

from edulib.core import (
    bus,
)
from edulib.core.base.tests.utils import (
    randint,
)

from .. import (
    domain,
)


class ServicesTestCase(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.repository = bus.get_uow().academic_years
        cls.external_id = randint()
        cls.initial_data = {
            'id': cls.external_id,
            'code': '2001/2002',
            'name': '2001/2001',
            'date_begin': '01.09.2001',
            'date_end': '31.08.2002',
        }
        cls.changed_data = {
            'id': cls.external_id,
            'code': '2002/2003',
            'name': '2002/2003',
            'date_begin': '01.09.2002',
            'date_end': '31.08.2003',
        }

    def test_events_created(self):
        bus.handle(domain.AcademicYearCreated(**self.initial_data))

        result = self.repository.get_object_by_id(self.external_id)
        self.assertIsNotNone(result.id)

        for attname, value in self.initial_data.items():
            with self.subTest(attname):
                result_value = getattr(result, attname)
                if isinstance(result_value, date):
                    result_value = result_value.strftime('%d.%m.%Y')
                self.assertEqual(result_value, value)

    def test_events_updated(self):
        self.repository.add(domain.AcademicYear(**self.initial_data))
        self.repository.get_object_by_id(self.external_id)

        bus.handle(domain.AcademicYearUpdated(**self.changed_data))

        result = self.repository.get_object_by_id(self.external_id)

        for attname, value in self.changed_data.items():
            with self.subTest(attname):
                result_value = getattr(result, attname)
                if isinstance(result_value, date):
                    result_value = result_value.strftime('%d.%m.%Y')
                self.assertEqual(result_value, value)

    def test_events_deleted(self):
        self.repository.add(domain.AcademicYear(**self.initial_data))
        self.repository.get_object_by_id(self.external_id)

        bus.handle(domain.AcademicYearDeleted(**self.changed_data))

        with self.assertRaises(domain.AcademicYearNotFound):
            self.repository.get_object_by_id(self.external_id)
