from io import (
    BytesIO,
)
from typing import (
    Any,
)

import pandas as pd
from django.urls import (
    reverse,
)
from rest_framework import (
    status,
)
from rest_framework.test import (
    APITransactionTestCase,
)

from edulib.core import (
    bus,
)
from edulib.core.federal_books.constants import (
    COLUMN_AUTHOR,
    COLUMN_CLASS,
    COLUMN_NAME,
    COLUMN_PUBLISHER,
    COLUMN_ROW_NUM,
)
from edulib.core.federal_books.tests.utils import (
    get_fed_book,
)
from edulib.core.lib_authors.tests.utils import (
    get_author,
)
from edulib.core.lib_publishings.tests.utils import (
    get_publishing,
)
from edulib.core.parallels.tests.utils import (
    get_parallel,
)


class ImportBooksTestCase(APITransactionTestCase):
    """Тесты загрузки файлов для импорта книг."""

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.url = reverse('fed_books-import-books')

    def create_test_xlsx(self, data) -> BytesIO:
        """Создает временный xlsx файл из переданных данных."""
        df = pd.DataFrame(data)
        file = BytesIO()
        df.to_excel(file, index=False)
        file.seek(0)
        file.name = 'test.xlsx'
        return file

    def test_upload_non_xlsx_file(self) -> None:
        """Тест попытки загрузить файл в неверном формате."""
        file_content = b"this is not an xlsx file"
        file = BytesIO(file_content)
        file.name = 'test.txt'

        response = self.client.post(self.url, {'file': file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.json())
        self.assertEqual(response.json()['non_field_errors'][0], 'Приложен некорректный тип файла.')

    def test_upload_xlsx_file(self) -> None:
        """Тест загрузки корректного xlsx файла."""
        # Создание временного xlsx файла
        data = {
            COLUMN_NAME: ['Математика'],
            COLUMN_AUTHOR: ['Иванов И.И.'],
            COLUMN_CLASS: ['1'],
            COLUMN_PUBLISHER: ['Издательство 1'],
            COLUMN_ROW_NUM: [1]
        }
        file = self.create_test_xlsx(data)

        response = self.client.post(self.url, {'file': file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content_disposition = response.get('Content-Disposition')
        self.assertIn('attachment; filename="log_changes.csv"', content_disposition)
        self.assertEqual(response['Content-Type'], 'text/csv')

    def test_upload_xlsx_file_with_missing_columns(self) -> None:
        """Тест загрузки xlsx файла с отсутствующими данными в обязательных столбцах."""
        data = {
            COLUMN_NAME: ['Математика'],
            COLUMN_CLASS: ['1'],
            COLUMN_PUBLISHER: ['Издательство 1'],
            COLUMN_ROW_NUM: [1],
            COLUMN_AUTHOR: [None]  # Отсутствуют данные в обязательном столбце
        }
        file = self.create_test_xlsx(data)

        response = self.client.post(self.url, {'file': file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content_disposition = response.get('Content-Disposition')
        self.assertIn('attachment; filename="log_changes.csv"', content_disposition)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn(f'Ошибка: Строка 1 не указан обязательный атрибут {COLUMN_AUTHOR}', content)

    def test_upload_xlsx_file_with_duplicates(self) -> None:
        """Тест загрузки xlsx файла с дублирующимися строками."""
        data = {
            COLUMN_NAME: ['Математика', 'Математика'],
            COLUMN_AUTHOR: ['Иванов И.И.', 'Иванов И.И.'],
            COLUMN_CLASS: ['1', '1'],
            COLUMN_PUBLISHER: ['Издательство 1', 'Издательство 1'],
            COLUMN_ROW_NUM: [1, 2]
        }
        file = self.create_test_xlsx(data)

        response = self.client.post(self.url, {'file': file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content_disposition = response.get('Content-Disposition')
        self.assertIn('attachment; filename="log_changes.csv"', content_disposition)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn('Ошибка: Строка 2 является дублем строки 1. Запись будет пропущена', content)


class FedBookRestTestCase(APITransactionTestCase):

    def setUp(self) -> None:
        self.uow = bus.get_uow()
        self.parallel = get_parallel(self.uow)
        self.author = get_author(self.uow)
        self.publishing = get_publishing(self.uow)
        self.fed_book = get_fed_book(
            self.uow,
            author_id=self.author.id,
            publishing_id=self.publishing.id,
            parallel_id=self.parallel.id,
        )
        self.list_url = reverse('fed_books-list')
        self.detail_url = reverse('fed_books-detail', args=[self.fed_book.id])

    def test_list(self) -> None:
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ('count', 'next', 'previous', 'results'):
            with self.subTest(field=field):
                self.assertIn(field, response.data)
        self.assert_fed_book(response.json()['results'][0])

    def test_detail(self) -> None:
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assert_fed_book(response.json())

    def test_search_by_fields(self) -> None:
        search_fields = {
            'author__name': self.author.name,
            'code': self.fed_book.code,
            'parallel__title': self.parallel.title,
            'publishing__name': self.publishing.name,
            'validity_period': self.fed_book.validity_period,
        }

        for field, value in search_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {'search': value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertGreater(len(results), 0)
                self.assert_fed_book(results[0])

    def test_search_by_nonexistent_values(self) -> None:
        search_fields = {
            'author__name': 'NonExistentName',
            'code': '000000',
            'parallel__title': 'NonExistentParallel',
            'publishing__name': 'NonExistentName',
            'validity_period': '2999-10-10',
        }

        for field, value in search_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {'search': value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertEqual(len(results), 0)

    def test_filter_by_fields(self) -> None:
        filter_fields = {
            'author_id': self.author.id,
            'publishing_id': self.publishing.id,
            'pub_lang': self.fed_book.pub_lang,
            'status': self.fed_book.status,
        }

        for field, value in filter_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, data={field: value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']
                self.assertGreater(len(results), 0)
                self.assert_fed_book(results[0])

    def test_filter_by_nonexistent_values(self) -> None:
        filter_fields = {
            'author_id': 9999,
            'publishing_id': 9999,
            'pub_lang': 'NonExistentLang',
            'status': False,
        }

        for field, value in filter_fields.items():
            with self.subTest(field=field):
                response = self.client.get(self.list_url, {field: value})
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                results = response.json()['results']

                self.assertEqual(len(results), 0)

    def assert_fed_book(self, fed_book: dict[str, Any]) -> None:
        self.assertDictEqual(
            fed_book,
            {
                'id': self.fed_book.id,
                'name': self.fed_book.name,
                'author': {
                    'id': self.author.id,
                    'name': self.author.name,
                },
                'publishing': {
                    'id': self.publishing.id,
                    'name': self.publishing.name,
                },
                'pub_lang': self.fed_book.pub_lang,
                'status': self.fed_book.status,
                'code': self.fed_book.code,
                'validity_period': self.fed_book.validity_period.isoformat(),
                'training_manuals': self.fed_book.training_manuals,
                'parallel': [self.parallel.id, ]
            },
        )
