from django.core.files.uploadedfile import (
    SimpleUploadedFile,
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

from edulib.core.lib_passport.adapters.db import (
    passport_repository,
    work_mode_repository,
)
from edulib.core.lib_passport.cleanup_days.adapters.db import (
    repository as cleanup_day_repo,
)
from edulib.core.lib_passport.cleanup_days.domain.model import (
    CleanupDay,
)
from edulib.core.lib_passport.documents.adapters.db import (
    repository as document_repo,
)
from edulib.core.lib_passport.documents.domain import (
    Document,
)
from edulib.core.lib_passport.domain.model import (
    Passport,
    WorkMode,
)
from edulib.core.schools.adapters.db import (
    repository as school_repo,
)
from edulib.core.schools.domain.model import (
    School,
)


class BasePassportTestCase(APITransactionTestCase):
    """Базовый тестовый класс для настройки общих данных."""

    def setUp(self):
        """Подготавливает общие данные для тестов."""
        self.school = school_repo.add(School(short_name='Школа №1', id=4815162342, status=True))


class LibPassportTestCase(BasePassportTestCase):
    """Тесты для эндпоинтов паспорта библиотеки."""

    def setUp(self):
        """Подготавливает данные для тестов."""
        super().setUp()
        self.lib_passport_data = {
            'school_id': self.school.id,
            'name': 'Библиотека школы №1',
            'date_found_month': 1,
            'date_found_year': 1990,
            'is_address_match': True,
            'is_telephone_match': False,
            'telephone': '1234567890',
            'is_email_match': False,
            'email': 'library@school.com',
        }

    def test_create_lib_passport(self):
        """Тест создания паспорта библиотеки."""
        response = self.client.post(reverse('libraries-list'), self.lib_passport_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        for field, value in self.lib_passport_data.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_update_lib_passport(self):
        """Тест обновления паспорта библиотеки."""
        lib_passport = passport_repository.add(Passport(**self.lib_passport_data))
        updated_fields = {
            'name': 'Обновленная библиотека школы №1',
            'telephone': '9876543210'
        }

        response = self.client.patch(reverse('libraries-detail', args=[lib_passport.id]), updated_fields)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_delete_lib_passport(self):
        """Тест удаления паспорта библиотеки."""
        lib_passport = passport_repository.add(Passport(**self.lib_passport_data))

        response = self.client.delete(reverse('libraries-detail', args=[lib_passport.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class WorkModeTestCase(BasePassportTestCase):
    """Тесты для эндпоинтов режима работы библиотеки."""

    def setUp(self):
        """Подготавливает данные для тестов."""
        super().setUp()
        self.lib_passport = passport_repository.add(Passport(school_id=self.school.id, name='Библиотека школы №1'))
        self.work_mode_data = {'lib_passport_id': self.lib_passport.id, 'schedule_mon_from': '9:00'}

    def test_create_work_mode(self):
        """Тест создания режима работы библиотеки."""
        url = reverse('work-modes-list', kwargs={'lib_passport_id': self.lib_passport.id})
        response = self.client.post(url, self.work_mode_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        for field, value in self.work_mode_data.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_update_work_mode(self):
        """Тест обновления режима работы библиотеки."""
        work_mode = work_mode_repository.add(WorkMode(**self.work_mode_data))
        updated_fields = {
            'schedule_mon_from': '8:00',
            'schedule_mon_to': '17:00',
        }

        response = self.client.patch(reverse(
            'work-modes-detail',
            args=[self.lib_passport.id, work_mode.id]),
            updated_fields
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_delete_work_mode(self):
        """Тест удаления режима работы библиотеки."""
        work_mode = work_mode_repository.add(WorkMode(**self.work_mode_data))

        response = self.client.delete(reverse('work-modes-detail', args=[self.lib_passport.id, work_mode.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class DocumentTestCase(BasePassportTestCase):
    """Тесты для эндпоинтов документов библиотеки."""

    def setUp(self):
        """Подготавливает данные для тестов."""
        super().setUp()
        self.lib_passport = passport_repository.add(Passport(school_id=self.school.id, name='Библиотека школы №1'))
        self.document_data = {
            'library_passport_id': self.lib_passport.id,
            'doc_type': 1,
            'name': 'Документ 1',
            'document': SimpleUploadedFile("test_document.txt", b"Content of the test document.")
        }

    def test_create_document(self):
        """Тест создания документа библиотеки."""
        url = reverse('documents-list', kwargs={'lib_passport_id': self.lib_passport.id})

        response = self.client.post(url, self.document_data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        for field, value in self.document_data.items():
            if field != 'document':
                with self.subTest(field=field):
                    self.assertEqual(response.data[field], value)

    def test_update_document(self):
        """Тест обновления документа библиотеки."""
        document = document_repo.add(Document(**self.document_data))
        updated_fields = {
            'name': 'Обновленный документ',
            'doc_type': 2,
        }

        response = self.client.patch(reverse(
            'documents-detail',
            args=[self.lib_passport.id, document.id]),
            updated_fields, format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_delete_document(self):
        """Тест удаления документа библиотеки."""
        document = document_repo.add(Document(**self.document_data))

        response = self.client.delete(reverse('documents-detail', args=[self.lib_passport.id, document.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CleanupDayTestCase(BasePassportTestCase):
    """Тесты для эндпоинтов санитарных дней."""

    def setUp(self):
        """Подготавливает данные для тестов."""
        super().setUp()
        self.lib_passport = passport_repository.add(Passport(school_id=self.school.id, name='Библиотека школы №1'))
        self.cleanup_day_data = {'cleanup_date': '2024-07-01', 'lib_passport_id': self.lib_passport.id}

    def test_create_cleanup_day(self):
        """Тест создания санитарного дня."""
        url = reverse('cleanup-days-list', kwargs={'lib_passport_id': self.lib_passport.id})
        response = self.client.post(url, self.cleanup_day_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        for field, value in self.cleanup_day_data.items():
            with self.subTest(field=field):
                self.assertEqual(response.data[field], value)

    def test_list_cleanup_days(self):
        """Тест получения списка санитарных дней."""
        cleanup_day_repo.add(CleanupDay(**self.cleanup_day_data))
        cleanup_day_repo.add(CleanupDay(lib_passport_id=self.lib_passport.id, cleanup_date='2024-08-01'))

        url = reverse('cleanup-days-list', args=[self.lib_passport.id])
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_cleanup_day(self):
        """Тест получения конкретного санитарного дня."""
        cleanup_day = cleanup_day_repo.add(CleanupDay(**self.cleanup_day_data))

        url = reverse('cleanup-days-detail', kwargs={'lib_passport_id': self.lib_passport.id, 'pk': cleanup_day.id})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], cleanup_day.id)

    def test_delete_cleanup_day(self):
        """Тест удаления санитарного дня."""
        cleanup_day = cleanup_day_repo.add(CleanupDay(**self.cleanup_day_data))

        response = self.client.delete(reverse('cleanup-days-detail', args=[self.lib_passport.id, cleanup_day.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
