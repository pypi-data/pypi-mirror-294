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
    APITransactionTestCase,
)

from edulib.core.directory.adapters.db import (
    repository,
)
from edulib.core.directory.domain import (
    Bbk,
)


class RestBbkTestCase(APITransactionTestCase):
    """Тесты справочника "Разделы ББК"."""

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.bbk = {
            'code': '42.11',
            'name': 'Зерновые и зернобобовые культуры',
        }
        self.bbk1 = repository.add(Bbk(code='22.98', name='Физика'))
        self.list_url = reverse('bbk-list')

    def test_create_bbk(self) -> None:
        """Тест создания раздела ББК."""
        response = self.client.post(self.list_url, self.bbk)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        for field, value in self.bbk.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_patch_bbk(self) -> None:
        """Тест изменения раздела ББК."""
        bbk = repository.add(Bbk(**self.bbk))
        updated_fields = {
            'code': '42.112',
            'name': 'Зерновые культуры',
        }

        response = self.client.patch(reverse('bbk-detail', args=[bbk.id]), updated_fields)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_delete_bbk(self) -> None:
        """Тест удаления раздела ББК."""
        bbk = repository.add(Bbk(**self.bbk))

        response = self.client.delete(reverse('bbk-detail', args=[bbk.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_by_fields(self) -> None:
        """Тест поиска разделов ББК по полям code и name."""
        search_fields = {
            'code': self.bbk1.code,
            'name': self.bbk1.name,
        }

        for field, value in search_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {'search': value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertGreater(len(results), 0)
                self.assert_bbk(results[0])

    def test_search_by_nonexistent_values(self) -> None:
        """Тест поиска с несуществующими значениями."""
        search_fields = {
            'code': '00000',
            'name': 'Несуществующее имя',
        }

        for field, value in search_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {'search': value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertEqual(len(results), 0)

    def test_filter_by_fields(self) -> None:
        """Тест фильтрации разделов ББК по полям code и name."""
        filter_fields = {
            'code': self.bbk1.code,
            'name': self.bbk1.name,
        }

        for field, value in filter_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {field: value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertGreater(len(results), 0)
                self.assert_bbk(results[0])

    def test_filter_by_nonexistent_values(self) -> None:
        """Тест фильтрации с несуществующими значениями."""
        filter_fields = {
            'code': '00000',
            'name': 'Несуществующее имя',
        }

        for field, value in filter_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {field: value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertEqual(len(results), 0)

    def assert_bbk(self, bbk: dict[str, Any]) -> None:
        """Проверка структуры данных раздела ББК."""
        self.assertDictEqual(
            bbk,
            {
                'id': bbk['id'],
                'code': bbk['code'],
                'name': bbk['name'],
                'parent_id': None,
                'is_leaf': True,
            },
        )
