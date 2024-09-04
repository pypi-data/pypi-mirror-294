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
        cls.repository = bus.get_uow().study_levels
        cls.external_id = 1
        cls.initial_data = {
            'id': cls.external_id,
            'name': 'Начальное общее образование',
            'short_name': 'НОО',
            'first_parallel_id': 1,
            'last_parallel_id': 4,
            'object_status': True
        }
        cls.changed_data = {
            'id': cls.external_id,
            'name': 'Основное общее образование',
            'short_name': 'ООО',
            'first_parallel_id': 5,
            'last_parallel_id': 9,
            'object_status': False
        }

    def test_events_created(self):
        bus.handle(domain.StudyLevelCreated(**self.initial_data))

        result = self.repository.get_object_by_id(self.external_id)
        self.assertIsNotNone(result.id)

        for attname, value in self.initial_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

    def test_events_updated(self):
        self.repository.add(domain.StudyLevel(**self.initial_data))
        self.repository.get_object_by_id(self.external_id)

        bus.handle(domain.StudyLevelUpdated(**self.changed_data))

        result = self.repository.get_object_by_id(self.external_id)

        for attname, value in self.changed_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

    def test_events_deleted(self):
        self.repository.add(domain.StudyLevel(**self.initial_data))
        self.repository.get_object_by_id(self.external_id)

        bus.handle(domain.StudyLevelDeleted(**self.changed_data))

        with self.assertRaises(domain.StudyLevelNotFound):
            self.repository.get_object_by_id(self.external_id)
