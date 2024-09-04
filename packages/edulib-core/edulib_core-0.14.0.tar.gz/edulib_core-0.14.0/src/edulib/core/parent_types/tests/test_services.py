from django.test.testcases import (
    TransactionTestCase,
)

from edulib.core import (
    bus,
)

from .. import (
    domain,
)


class ServicesTestCase(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.repository = bus.get_uow().parent_types
        cls.external_id = 11408
        cls.initial_data = {
            'id': cls.external_id,
            'name': 'Родитель',
            'code': '1',
            'status': True
        }
        cls.changed_data = {
            'id': cls.external_id,
            'name': 'Опекун',
            'code': '2',
            'status': False
        }

    def test_events_created(self):
        bus.handle(domain.ParentTypeCreated(**self.initial_data))

        result = self.repository.get_object_by_id(self.external_id)
        self.assertIsNotNone(result.id)

        for attname, value in self.initial_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

    def test_events_updated(self):
        self.repository.add(domain.ParentType(**self.initial_data))
        self.repository.get_object_by_id(self.external_id)

        bus.handle(domain.ParentTypeUpdated(**self.changed_data))

        result = self.repository.get_object_by_id(self.external_id)

        for attname, value in self.changed_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

    def test_events_deleted(self):
        self.repository.add(domain.ParentType(**self.initial_data))
        self.repository.get_object_by_id(self.external_id)

        bus.handle(domain.ParentTypeDeleted(**self.initial_data))

        with self.assertRaises(domain.ParentTypeNotFound):
            self.repository.get_object_by_id(self.external_id)
