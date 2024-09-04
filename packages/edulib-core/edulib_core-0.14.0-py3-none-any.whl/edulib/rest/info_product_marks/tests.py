from django.urls import (
    reverse,
)
from rest_framework import (
    status,
)
from rest_framework.test import (
    APITestCase,
)


class LibMarkInformProductTests(APITestCase):
    """Тесты справочника "Знак информационной продукции"."""

    def setUp(self):
        """Подготавливает данные для тестов."""
        self.test_data = {'code': 'test_code', 'name': 'test_name'}
        self.detail_url = reverse('info_product_marks-detail', args=[1])
        self.list_url = reverse('info_product_marks-list')

    def test_retrieve_info_product_marks_list(self):
        """Тест получения списка всех записей в справочнике "Знак информационной продукции"."""
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)

    def test_retrieve_specific_info_product_marks_by_id(self):
        """Тест получения конкретной записи по ID в справочнике "Знак информационной продукции"."""
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['name'], 'для детей всех возрастов')

    def test_search_info_product_marks(self):
        """Тест функции поиска по полю 'name' в справочнике "Знак информационной продукции"."""
        response = self.client.get(self.list_url, {'search': 'запрещено для детей'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'запрещено для детей')

    def test_info_product_marks_not_allowed_methods(self):
        """Тест запрета методов POST, PUT, PATCH и DELETE для справочника "Знак информационной продукции"."""
        requests = [
            ('post', self.list_url, self.test_data),
            ('put', self.detail_url, self.test_data),
            ('patch', self.detail_url, self.test_data),
            ('delete', self.detail_url, {}),
        ]

        for method, url, data in requests:
            with self.subTest(method=method):
                response = getattr(self.client, method)(url, data)

                self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_ordering_info_product_marks_by_code(self):
        """Тест сортировки записей по полю 'code' в справочнике "Знак информационной продукции"."""
        response = self.client.get(self.list_url, {'ordering': 'code'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        sorted_codes = ['0+', '6+', '12+', '16+', '18+']
        results_codes = [item['code'] for item in response.data['results']]
        self.assertEqual(results_codes, sorted_codes)

        response = self.client.get(self.list_url, {'ordering': '-code'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        sorted_codes_desc = ['18+', '16+', '12+', '6+', '0+']
        results_codes_desc = [item['code'] for item in response.data['results']]
        self.assertEqual(results_codes_desc, sorted_codes_desc)
