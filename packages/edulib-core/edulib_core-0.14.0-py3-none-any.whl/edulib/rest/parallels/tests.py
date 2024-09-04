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
from edulib.core.parallels.domain import (
    Parallel,
)


class ParallelsTests(APITestCase):
    """Тесты справочника "Параллели"."""

    def setUp(self):
        """Подготавливает данные для тестов."""
        self.initial_data = {
            'id': 200,
            'title': '1я параллель',
            'object_status': True,
        }
        self.parallel = bus.get_uow().parallels.add(
            Parallel(
                id=self.initial_data['id'],
                title=self.initial_data['title'],
                system_object_id=200,
                object_status=self.initial_data['object_status'],
            ),
        )
        self.detail_url = reverse('parallels-detail', args=[self.parallel.id])
        self.list_url = reverse('parallels-list')

    def test_retrieve_parallels(self):
        """Тест получения списка всех записей в справочнике "Параллели"."""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ('count', 'next', 'previous', 'results'):
            with self.subTest(field=field):
                self.assertIn(field, response.data)

        self.assertIsInstance(response.data['results'], list)
        first_result = response.data['results'][0]
        for field, expected_value in self.initial_data.items():
            with self.subTest(result_field=field):
                self.assertIn(field, first_result)
                self.assertEqual(first_result[field], expected_value)

    def test_retrieve_specific_parallel_by_id(self):
        """Тест получения конкретной записи по ID в справочнике "Параллели"."""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field, expected_value in self.initial_data.items():
            with self.subTest(field=field):
                self.assertIn(field, response.data)
                self.assertEqual(response.data[field], expected_value)

    def test_parallels_not_allowed_methods(self):
        """Тест запрета методов POST, PUT, PATCH и DELETE для справочника "Параллели"."""
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
