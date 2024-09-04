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
        cls.repository = bus.get_uow().disciplines
        cls.external_id = randint()
        cls.initial_data = {
            'id': cls.external_id,
            'name': 'Предмет 1',
        }
        cls.changed_data = {
            'id': cls.external_id,
            'name': 'Предмет 2',
            'description': (
                'Учебный предмет (учебная дисциплина) - система знаний, умений и навыков, отобранных из определенной '
                'отрасли науки, техники, искусства, производственной деятельности для изучения в учебном заведении. '
                'По содержанию бывает общеобразовательным (общенаучным) или специальным, определяющим профиль '
                'подготовки специалиста.'
            )
        }

    def test_events_created(self):
        bus.handle(domain.DisciplineCreated(**self.initial_data))

        result = self.repository.get_object_by_id(self.external_id)
        self.assertIsNotNone(result.id)

        for attname, value in self.initial_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

    def test_events_updated(self):
        self.repository.add(domain.factory.create(domain.DisciplineDTO(**self.initial_data)))
        self.repository.get_object_by_id(self.external_id)

        bus.handle(domain.DisciplineUpdated(**self.changed_data))

        result = self.repository.get_object_by_id(self.external_id)

        for attname, value in self.changed_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

    def test_events_deleted(self):
        self.repository.add(domain.factory.create(domain.DisciplineDTO(**self.initial_data)))
        self.repository.get_object_by_id(self.external_id)

        bus.handle(domain.DisciplineDeleted(**self.changed_data))

        with self.assertRaises(domain.DisciplineNotFound):
            self.repository.get_object_by_id(self.external_id)
