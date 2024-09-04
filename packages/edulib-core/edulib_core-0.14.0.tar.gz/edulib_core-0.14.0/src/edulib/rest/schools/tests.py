from typing import (
    Any,
)

from django.urls import (
    reverse,
)
from rest_framework import (
    status,
)
from rest_framework.test import (
    APITestCase,
)

from edulib.core import (
    bus,
)
from edulib.core.address.tests.utils import (
    get_address,
)
from edulib.core.institution_types.tests.utils import (
    get_institution_type,
)
from edulib.core.schools.tests.utils import (
    get_school,
)


class SchoolRestTestCase(APITestCase):
    """Тесты справочника "Организации"."""

    def setUp(self) -> None:
        self.maxDiff = None
        self.uow = bus.get_uow()

        self.address = get_address(self.uow)
        self.institution_type = get_institution_type(self.uow)
        self.school = get_school(
            self.uow,
            institution_type_id=self.institution_type.id,
            f_address_id=self.address.id,
            u_address_id=self.address.id,
        )
        self.list_url = reverse('schools-list')
        self.detail_url = reverse('schools-detail', args=[self.school.id])

    def test_list(self) -> None:
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ('count', 'next', 'previous', 'results'):
            with self.subTest(field=field):
                self.assertIn(field, response.data)
        self.assert_school(response.json()['results'][0])

    def test_detail(self) -> None:
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_school(response.json())

    def test_not_allowed_methods(self) -> None:
        requests = (
            ('post', self.list_url),
            ('put', self.detail_url),
            ('patch', self.detail_url),
            ('delete', self.detail_url),
        )

        for method, url in requests:
            with self.subTest(method=method):
                response = self.client.generic(method, url)
                self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_search_by_fields(self) -> None:
        search_fields = {
            'name': self.school.name,
            'short_name': self.school.short_name,
            'institution_type_id': self.institution_type.id,
        }

        for field, value in search_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {'search': value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertGreater(len(results), 0)
                self.assert_school(results[0])

    def test_search_by_nonexistent_values(self) -> None:
        search_fields = {
            'name': 'NonExistentName',
            'short_name': 'NonExistentShortName',
            'institution_type_id': 99999,
        }

        for field, value in search_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {'search': value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertEqual(len(results), 0)

    def assert_school(self, school: dict[str, Any]) -> None:
        self.assertDictEqual(
            school,
            {
                'id': self.school.id,
                'short_name': self.school.short_name,
                'name': self.school.name,
                'kpp': self.school.kpp,
                'okato': self.school.okato,
                'oktmo': self.school.oktmo,
                'okpo': self.school.okpo,
                'ogrn': self.school.ogrn,
                'inn': self.school.inn,
                'telephone': self.school.telephone,
                'email': self.school.email,
                'website': self.school.website,
                'fax': self.school.fax,
                'manager': self.school.manager,
                'institution_type': {
                    'id': str(self.institution_type.id),
                    'name': self.institution_type.name,
                },
                'parent_id': None,
                'f_addr': {
                    'id': str(self.address.id),
                    'full_address': self.address.full,
                },
                'u_addr': {
                    'id': str(self.address.id),
                    'full_address': self.address.full,
                },
            },
        )
