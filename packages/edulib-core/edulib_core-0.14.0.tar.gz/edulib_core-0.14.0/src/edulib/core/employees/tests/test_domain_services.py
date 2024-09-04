import datetime

from dateutil.relativedelta import (
    relativedelta,
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
from edulib.core.persons.tests.utils import (
    get_person,
)
from edulib.core.schools.tests.utils import (
    get_school,
)

from .. import (
    domain,
)
from .utils import (
    get_employee,
)


class TestCase(TransactionTestCase):

    def setUp(self):
        self.uow = bus.get_uow()
        self.person = get_person(self.uow)
        self.school = get_school(self.uow)

        self.employee_params = {
            'id': randint(),
            'person_id': self.person.id,
            'school_id': self.school.id,
            'info_date_begin': datetime.date.today() - relativedelta(years=1),
            'info_date_end': None,
            'job_code': 1,
            'job_name': 'Директор',
            'employment_kind_id': 1,
            'personnel_num': '001',
            'object_status': True
        }
        self.update_params = self.employee_params | {
            'info_date_begin': datetime.date.today() - relativedelta(years=2),
            'info_date_end': datetime.date.today() + relativedelta(days=14),
            'job_code': 2,
            'job_name': 'Завхоз',
            'employment_kind_id': 2,
            'personnel_num': '002',
        }

    def test_create_employee(self):
        with self.uow.wrap() as uow:
            employee = domain.create_employee(domain.EmployeeDTO(**self.employee_params), uow)

        self.assertIsNotNone(employee.id)

        for attname, value in self.employee_params.items():
            with self.subTest(attname):
                self.assertEqual(getattr(employee, attname), value)

    def test_update_employee(self):
        with self.uow.wrap() as uow:
            employee = get_employee(uow, **self.employee_params)

            domain.update_employee(employee, domain.EmployeeDTO(**self.update_params), uow)
            employee = uow.employees.get_object_by_id(employee.id)

            for attname, value in self.update_params.items():
                with self.subTest(attname):
                    self.assertEqual(getattr(employee, attname), value)

    def test_delete_employee(self):
        with self.uow.wrap() as uow:
            employee = get_employee(uow, **self.employee_params)

            domain.delete_employee(domain.EmployeeDTO(**self.employee_params), uow)

            with self.assertRaises(domain.EmployeeNotFound):
                uow.employees.get_object_by_id(employee.id)
