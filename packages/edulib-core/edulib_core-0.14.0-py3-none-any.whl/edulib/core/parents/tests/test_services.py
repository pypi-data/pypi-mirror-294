from django.test.testcases import (
    TransactionTestCase,
)

from edulib.core import (
    bus,
)
from edulib.core.base.tests.utils import (
    randint,
)
from edulib.core.parent_types.tests.utils import (
    get_parent_type,
)
from edulib.core.parents.tests.utils import (
    get_parent,
)
from edulib.core.persons.tests.utils import (
    get_person,
)

from .. import (
    domain,
)


class ServicesTestCase(TransactionTestCase):

    def setUp(self) -> None:
        self.uow = bus.get_uow()

        self.parent_id = randint()
        self.person = get_person(self.uow)
        self.child_1 = get_person(self.uow)
        self.child_2 = get_person(self.uow)
        self.parent_type_parent = get_parent_type(self.uow)
        self.parent_type_agent = get_parent_type(self.uow, name='Представитель')

        self.initial_data = {
            'id': self.parent_id,
            'parent_person_id': self.person.id,
            'child_person_id': self.child_1.id,
            'parent_type_id': self.parent_type_agent.id,
            'status': True
        }

        self.changed_data = {
            'id': self.parent_id,
            'child_person_id': self.child_2.id,
            'parent_type_id': self.parent_type_agent.id,
            'status': False
        }

    def test_parent_created(self):
        bus.handle(domain.ParentCreated(**self.initial_data))

        initial_parent = self.uow.parents.get_object_by_id(self.parent_id)

        for attname, value in self.initial_data.items():
            result = getattr(initial_parent, attname)
            self.assertEqual(result, value)

    def test_parent_updated(self):
        get_parent(self.uow, **self.initial_data)

        bus.handle(domain.ParentUpdated(**self.changed_data))

        changed_parent = self.uow.parents.get_object_by_id(self.parent_id)

        for attname, value in (self.initial_data | self.changed_data).items():
            result = getattr(changed_parent, attname)
            self.assertEqual(result, value)

    def test_parent_deleted(self):
        get_parent(self.uow, **self.initial_data)

        bus.handle(domain.ParentDeleted(**self.initial_data))

        with self.assertRaises(domain.ParentNotFound):
            self.uow.parents.get_object_by_id(self.parent_id)
