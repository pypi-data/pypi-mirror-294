from datetime import (
    date,
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
from edulib.core.academic_years.domain.model import (
    AcademicYear,
)


class AcademicYearRestTestCase(APITestCase):
    """Тесты справочника "Периоды обучения"."""

    @classmethod
    def setUpClass(cls: 'AcademicYearRestTestCase') -> None:
        super().setUpClass()

        academic_year = bus.get_uow().academic_years.add(
            AcademicYear(
                id=10_000,
                code='23/24',
                name='2023/2024',
                date_begin=date(2023, 9, 1),
                date_end=date(2024, 8, 31),
            )
        )
        cls.list_url = reverse('academic-years-list')
        cls.detail_url = reverse('academic-years-detail', args=[academic_year.id])

    def test_list(self) -> None:
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ('count', 'next', 'previous', 'results'):
            with self.subTest(field=field):
                self.assertIn(field, response.data)

    def test_detail(self) -> None:
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ('id', 'code', 'name', 'date_begin', 'date_end'):
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
