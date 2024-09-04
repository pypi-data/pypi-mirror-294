import secrets

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
        cls.repository = bus.get_uow().municipal_units

        cls.external_id = secrets.randbits(63)

        cls.initial_data = {
            'id': cls.external_id,
            'name': 'Наименование 1',
            'oktmo': '12345678901',
            'constituent_entity': 'Санкт-Петербург'
        }
        cls.changed_data = {
            'id': cls.external_id,
            'name': 'Наименование 2',
            'oktmo': '12345678905',
            'constituent_entity': 'Севастополь'
        }

    def test_events_created(self):
        bus.handle(domain.MunicipalUnitCreated(**self.initial_data))

        result = self.repository.get_object_by_id(self.external_id)
        self.assertIsNotNone(result.id)

        for attname, value in self.initial_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

    def test_events_updated(self):
        self.repository.add(domain.MunicipalUnit(**self.initial_data))
        self.repository.get_object_by_id(self.external_id)

        bus.handle(domain.MunicipalUnitUpdated(**self.changed_data))

        result = self.repository.get_object_by_id(self.external_id)

        for attname, value in self.changed_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

    def test_events_deleted(self):
        self.repository.add(domain.MunicipalUnit(**self.initial_data))
        self.repository.get_object_by_id(self.external_id)

        bus.handle(domain.MunicipalUnitDeleted(**self.changed_data))

        with self.assertRaises(domain.MunicipalUnitNotFound):
            self.repository.get_object_by_id(self.external_id)
