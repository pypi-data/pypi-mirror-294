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

from edulib.core.lib_passport.models import (
    LibPassport,
)
from edulib.core.library_event import (
    domain,
)
from edulib.core.library_event.adapters.db import (
    repository,
)
from edulib.core.schools.models import (
    School,
)


class RestEventTestCase(TransactionTestCase):
    """Тесты реестра "План работы библиотеки"."""

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.client = APIClient()
        school = School.objects.create(
            id=4815162342,
            short_name='СОШ №7',
            status=True,
        )
        library = LibPassport.objects.create(
            school_id=school.id,
            name='Библиотека',
        )
        self.event = {
            'library_id': library.id,
            'date_begin': '2023-01-20',
            'date_end': '2023-01-25',
            'name': 'Читаем поэмы',
            'participants': 'Учителя, ученики',
            'description': 'Пройдёт мероприятие по чтению поэм',
            'place': 'Библиотека',
        }

    def test_create_event(self) -> None:
        """Тест создания плана работы библиотеки."""
        response = self.client.post(reverse('events-list'), self.event)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        for field, value in self.event.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_update_event(self) -> None:
        """Тест обновления плана работы библиотеки."""
        event = repository.add(domain.Event(**self.event))
        updated_fields = {
            'date_begin': '2023-01-21',
            'date_end': '2023-02-25',
            'name': 'Читаем стихи',
            'participants': 'Учителя, ученики, родители',
            'description': 'Пройдёт мероприятие по чтению стихов',
            'place': 'Кабинет русского языка',
        }

        response = self.client.patch(reverse('events-detail', args=[event.id]), updated_fields)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_delete_event(self) -> None:
        """Тест удаления плана работы библиотеки."""
        event = repository.add(domain.Event(**self.event))

        response = self.client.delete(reverse('events-detail', args=[event.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
