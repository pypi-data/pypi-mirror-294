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
from edulib.core.disciplines.domain import (
    Discipline,
)


class DisciplineRestTests(APITestCase):
    """Тесты справочника "Предметы"."""

    @classmethod
    def setUpClass(cls: 'DisciplineRestTests') -> None:
        super().setUpClass()

        discipline = bus.get_uow().disciplines.add(
            Discipline(
                id=300,
                name='Русский язык',
            ),
        )
        cls.list_url = reverse('disciplines-list')
        cls.detail_url = reverse('disciplines-detail', args=[discipline.id])

    def test_list(self) -> None:
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ('count', 'next', 'previous', 'results'):
            with self.subTest(field=field):
                self.assertIn(field, response.data)

    def test_detail(self) -> None:
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in (
            'id',
            'name',
            'description',
        ):
            with self.subTest(field=field):
                self.assertIn(field, response.data)

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
