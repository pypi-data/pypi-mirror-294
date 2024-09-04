from django.test.testcases import (
    TransactionTestCase,
)

from edulib.core import (
    bus,
)
from edulib.core.address import (
    domain as addresses,
)
from edulib.core.address.tests.utils import (
    get_address,
)
from edulib.core.base.tests.utils import (
    randint,
)
from edulib.core.institution_types.tests.utils import (
    get_institution_type,
)
from edulib.core.municipal_units.tests.utils import (
    get_municipal_unit,
)
from edulib.core.schools.tests.utils import (
    get_school,
)

from .. import (
    domain,
)


class ServicesTestCase(TransactionTestCase):

    def setUp(self):
        self.uow = bus.get_uow()

        self.initial_municipal_unit = get_municipal_unit(
            self.uow,
            name='Наименование 1',
            constituent_entity='Родительская организация 1',
            oktmo='36634436111'
        )

        self.changed_municipal_unit = get_municipal_unit(
            self.uow,
            name='Наименование 2',
            constituent_entity='Родительская организация 2',
            oktmo='36634436112'
        )

        self.initial_institution_type = get_institution_type(self.uow)
        self.changed_institution_type = get_institution_type(
            self.uow,
            name='Муниципальное автономное образовательное учреждение',
            id=2
        )

        self.repository = self.uow.schools

        self.external_id = randint()

        self.initial_data = {
            'id': self.external_id,
            'short_name': 'Краткое наименование 1',
            'manager': 'Иванов Иван Иванович',
            'status': True,
            'name': 'Наименование 1',
            'inn': '123456789012',
            'kpp': '123456789',
            'okato': '123456789012',
            'oktmo': '12345678901',
            'okpo': '123456789012',
            'ogrn': '123456789012345',
            'telephone': '88006353535',
            'fax': '88006353535',
            'email': 'oo@example.com',
            'website': 'example.com',
            'parent': None,
            'territory_type_id': 1,
        }
        self.initial_addresses = {
            'f_address': 'г. Казань, ул. Вымышленная, д. 1',
            'u_address': 'г. Казань, ул. Вымышленная, д. 2',
        }
        self.changed_data = {
            'id': self.external_id,
            'short_name': 'Краткое наименование 2',
            'manager': 'Петров Петр Петрович',
            'status': True,
            'name': 'Наименование 2',
            'inn': '123456789010',
            'kpp': '123456780',
            'okato': '123456789010',
            'oktmo': '12345678900',
            'okpo': '123456789010',
            'ogrn': '123456789012340',
            'telephone': '88006353530',
            'fax': '88006353530',
            'email': 'oo@example2.com',
            'website': 'example2.com',
            'parent': None,
            'territory_type_id': 2,
        }
        self.changed_addresses = {
            'f_address': 'г. Казань, ул. Вымышленная, д. 2',
            'u_address': 'г. Казань, ул. Вымышленная, д. 1',
        }

    def test_events_created(self):
        bus.handle(domain.SchoolCreated(
            institution_type_id=self.initial_institution_type.id,
            municipal_unit_id=self.initial_municipal_unit.id,
            **self.initial_data | self.initial_addresses
        ))

        result = self.repository.get_object_by_id(self.external_id)
        self.assertIsNotNone(result.id)

        for attname, value in self.initial_data.items():
            with self.subTest(attname):
                self.assertEqual(getattr(result, attname), value)

        self.assertEqual(result.institution_type_id, self.initial_institution_type.id)
        self.assertEqual(result.municipal_unit_id, self.initial_municipal_unit.id)

        for attname, full_value in self.initial_addresses.items():
            address = self.uow.addresses.get_object_by_id(getattr(result, f'{attname}_id'))
            self.assertEqual(address.full, full_value)

    def test_events_updated(self):
        get_school(
            self.uow,
            institution_type_id=self.initial_institution_type.id,
            municipal_unit_id=self.initial_municipal_unit.id,
            **self.initial_data | {
                f'{attname}_id': get_address(self.uow, full=value).id
                for attname, value in self.initial_addresses.items()
            }
        )
        initial_result = self.repository.get_object_by_id(self.external_id)

        initial_address_ids = {
            attname: getattr(initial_result, f'{attname}_id')
            for attname in self.initial_addresses
        }

        bus.handle(domain.SchoolUpdated(
            institution_type_id=self.changed_institution_type.id,
            municipal_unit_id=self.changed_municipal_unit.id,
            **self.changed_data | self.changed_addresses
        ))

        result = self.repository.get_object_by_id(self.external_id)

        for attname, value in self.changed_data.items():
            self.assertEqual(getattr(result, attname), value)

        self.assertEqual(result.institution_type_id, self.changed_institution_type.id)
        self.assertEqual(result.municipal_unit_id, self.changed_municipal_unit.id)

        for attname, full_value in self.changed_addresses.items():
            address = self.uow.addresses.get_object_by_id(getattr(result, f'{attname}_id'))
            self.assertEqual(address.id, initial_address_ids[attname])
            self.assertEqual(address.full, full_value)

    def test_events_deleted(self):
        get_school(
            self.uow,
            institution_type_id=self.initial_institution_type.id,
            municipal_unit_id=self.initial_municipal_unit.id,
            **self.initial_data | {
                f'{attname}_id': get_address(self.uow, full=value).id
                for attname, value in self.initial_addresses.items()
            }
        )
        initial_result = self.repository.get_object_by_id(self.external_id)
        initial_address_ids = [
            getattr(initial_result, f'{attname}_id') for attname in self.initial_addresses
        ]

        bus.handle(domain.SchoolDeleted(**self.initial_data | self.initial_addresses))

        with self.assertRaises(domain.SchoolNotFound):
            self.repository.get_object_by_id(self.external_id)

        for address_id in initial_address_ids:
            with self.assertRaises(addresses.AddressNotFound):
                self.uow.addresses.get_object_by_id(address_id)
