from django.test import (
    TransactionTestCase,
)
from django.urls import (
    reverse,
)
from rest_framework import (
    status,
)
from rest_framework.test import (
    APIClient,
)

from edulib.core.lib_udc.adapters.db import (
    repository,
)
from edulib.core.lib_udc.domain.model import (
    Udc,
)


class UdcTestCase(TransactionTestCase):
    """Тесты справочника "Разделы УДК"."""

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.client = APIClient()
        self.udc = {
            'code': '621.396.677.41',
            'name': 'Бевериджа антенны',
        }

    def test_create_udc(self) -> None:
        """Тест создания раздела УДК."""
        response = self.client.post(reverse('udc-list'), self.udc)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        for field, value in self.udc.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_update_udc(self) -> None:
        """Тест обновления раздела УДК."""
        udc = repository.add(Udc(**self.udc))
        updated_fields = {
            'code': '621.396.677.4',
            'name': 'Волновые антенны',
        }

        response = self.client.patch(reverse('udc-detail', args=[udc.id]), updated_fields)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_delete_udc(self) -> None:
        """Тест удаления раздела УДК."""
        udc = repository.add(Udc(**self.udc))

        response = self.client.delete(reverse('udc-detail', args=[udc.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
