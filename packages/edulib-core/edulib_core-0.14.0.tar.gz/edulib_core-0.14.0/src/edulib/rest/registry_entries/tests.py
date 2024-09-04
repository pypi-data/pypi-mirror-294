import os
import tempfile
from datetime import (
    datetime,
    timedelta,
)
from typing import (
    Union,
)

from django.urls import (
    reverse,
)
from django.utils import (
    timezone,
)
from PIL import (
    Image,
)
from rest_framework import (
    status,
)
from rest_framework.test import (
    APITransactionTestCase,
)

from edulib.core.directory.models import (
    Catalog,
)
from edulib.core.disciplines.models import (
    Discipline,
)
from edulib.core.federal_books.models import (
    FederalBook,
)
from edulib.core.issuance_delivery.models import (
    IssuanceDelivery,
)
from edulib.core.lib_authors.models import (
    LibraryAuthors,
)
from edulib.core.lib_example_types.models import (
    LibraryExampleType,
)
from edulib.core.lib_publishings.models import (
    LibraryPublishings,
)
from edulib.core.lib_registry.domain import (
    EntryStatus,
)
from edulib.core.lib_registry.models import (
    LibMarkInformProduct,
    LibRegistryEntry,
    LibRegistryExample,
)
from edulib.core.lib_sources.models import (
    LibrarySource,
)
from edulib.core.lib_udc.models import (
    LibraryUDC,
)
from edulib.core.municipal_units.models import (
    MunicipalUnit,
)
from edulib.core.parallels.models import (
    Parallel,
)
from edulib.core.readers.models import (
    Reader,
)
from edulib.core.schools.models import (
    School,
)


class BaseEntryTestCase(APITransactionTestCase):
    @staticmethod
    def create_example(
        entry: LibRegistryEntry,
        publishing: LibraryPublishings,
        **kwargs: Union[str, int, datetime],
    ) -> LibRegistryExample:
        fields = {
            'lib_reg_entry': entry,
            'edition_year': 2020,
            'edition_place': 'Москва',
            'duration': 200,
            'publishing': publishing,
            'inflow_date': '2020-01-01',
            'book_code': '123',
            'edition': '1-е издание',
            'invoice_number': '1',
        } | kwargs

        return LibRegistryExample.objects.create(**fields)

    def setUp(self) -> None:
        self.age_tag, _ = LibMarkInformProduct.objects.get_or_create(id=3, code='12+', name='для детей старше 12 лет')
        self.municipal_unit = MunicipalUnit.objects.create(id=1, name='Адмиралтейский', constituent_entity='Спб')
        self.school = School.objects.create(
            id=200,
            short_name='МОУ СОШ №1',
            status=True,
            municipal_unit_id=self.municipal_unit.id,
        )
        self.author = LibraryAuthors.objects.create(name='Бархударов С.Г., Крючков С.Е., Максимов Л.Ю. и др.')
        self.discipline = Discipline.objects.create(name='Литература', id=100)
        self.source = LibrarySource.objects.create(name='Меценат 1')
        self.udc, _ = LibraryUDC.objects.get_or_create(id=10, code='8', name='Языкознание')
        self.bbc, _ = Catalog.objects.get_or_create(id=103, code='86.7', name='Свободомыслие')
        self.entry_type, _ = LibraryExampleType.objects.get_or_create(id=1, name='Учебник, учебная литература')
        self.parallel1 = Parallel.objects.create(
            title='Параллель 1',
            id=10_000,
            system_object_id=1,
            object_status=True,
        )
        self.parallel2 = Parallel.objects.create(
            title='Параллель 3',
            id=20_000,
            system_object_id=3,
            object_status=True,
        )

        self.entry = LibRegistryEntry.objects.create(
            title='Русский язык: 8-й класс: учебник',
            school_id=self.school.id,
            type_id=self.entry_type.id,
            age_tag=self.age_tag,
            udc=self.udc,
            bbc=self.bbc,
            discipline_id=self.discipline.id,
            author=self.author,
            source=self.source,
            short_info='Краткое описание',
        )
        self.entry.parallels.add(self.parallel1, self.parallel2)

        self.publishing1 = LibraryPublishings.objects.create(name='Дрофа')
        publishing2 = LibraryPublishings.objects.create(name='Питер')
        self.create_example(self.entry, self.publishing1)
        self.create_example(
            self.entry,
            publishing2,
            edition_year=2024,
            duration=250,
            book_code='321',
            edition='2-е издание',
        )
        self.create_example(self.entry, self.publishing1, writeoff_date=timezone.now() + timedelta(days=30))


class EntryRestTests(BaseEntryTestCase):
    """Тесты библиотечного реестра."""

    def setUp(self) -> None:
        super().setUp()

        self.create_example(self.entry, self.publishing1, writeoff_date=timezone.now() - timedelta(days=60))
        example_on_hand1 = self.create_example(self.entry, self.publishing1)
        example_on_hand2 = self.create_example(self.entry, self.publishing1)

        reader = Reader.objects.create()
        IssuanceDelivery.objects.create(
            example=example_on_hand1,
            issuance_date='2024-03-01',
            fact_delivery_date=timezone.now() + timedelta(days=30),
            reader=reader,
        )
        IssuanceDelivery.objects.create(
            example=example_on_hand2,
            issuance_date='2024-03-01',
            fact_delivery_date=timezone.now() - timedelta(days=60),
            reader=reader,
        )

        self.list_url = reverse('registry-entries-list')
        self.detail_url = reverse('registry-entries-detail', args=[self.entry.id])

    def test_list(self) -> None:
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ('count', 'next', 'previous', 'results'):
            with self.subTest(field=field):
                self.assertIn(field, response.data)
        self.assertDictEqual(
            response.json()['results'][0],
            {
                'id': self.entry.id,
                'type': {'id': self.entry_type.id, 'name': self.entry_type.name},
                'title': self.entry.title,
                'author': {'id': self.author.id, 'name': self.author.name},
                'parallels': [
                    {'id': self.parallel1.id, 'title': self.parallel1.title},
                    {'id': self.parallel2.id, 'title': self.parallel2.title},
                ],
                'udc': {'id': self.udc.id, 'name': self.udc.name, 'code': self.udc.code},
                'bbc': {'id': self.bbc.id, 'name': self.bbc.name, 'code': self.bbc.code},
                'discipline': {'id': self.discipline.id, 'name': self.discipline.name},
                'age_tag': {'id': self.age_tag.id, 'code': self.age_tag.code},
                'status': EntryStatus.CURRENT.label,
                'federal_book': None,
                'editions': '1-е издание, 2-е издание',
                'publishings': 'Дрофа, Питер',
                'publishing_years': '2020, 2024',
                'count': 5,
                'free_count': 4,
            },
        )

    def test_detail(self) -> None:
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                'id': self.entry.id,
                'type': {'id': self.entry_type.id, 'name': self.entry_type.name},
                'title': self.entry.title,
                'author': {'id': self.author.id, 'name': self.author.name},
                'parallels': [
                    {'id': self.parallel1.id, 'title': self.parallel1.title},
                    {'id': self.parallel2.id, 'title': self.parallel2.title},
                ],
                'udc': {'id': self.udc.id, 'name': self.udc.name, 'code': self.udc.code},
                'bbc': {'id': self.bbc.id, 'name': self.bbc.name, 'code': self.bbc.code},
                'source': {'id': self.source.id, 'name': self.source.name},
                'short_info': self.entry.short_info,
                'filename': self.entry.filename,
                'cover': self.entry.cover,
                'discipline': {'id': self.discipline.id, 'name': self.discipline.name},
                'age_tag': {'id': self.age_tag.id, 'code': self.age_tag.code},
                'status': EntryStatus.CURRENT.label,
                'federal_book': None,
                'editions': '1-е издание, 2-е издание',
                'publishings': 'Дрофа, Питер',
                'publishing_years': '2020, 2024',
                'count': 5,
                'free_count': 4,
            },
        )

    def test_create(self) -> None:
        initial_data = {
            'type_id': self.entry_type.id,
            'title': 'Математика: 5-й класс: базовый уровень: учебник: в 2 частях',
            'school_id': self.school.id,
            'author_id': self.author.id,
            'source_id': self.source.id,
            'short_info': 'Описание',
            'discipline_id': self.discipline.id,
            'age_tag_id': self.age_tag.id,
            'on_balance': True,
            'status': EntryStatus.CURRENT,
            'parallel_ids': [self.parallel1.id, self.parallel2.id],
        }

        response = self.client.post(self.list_url, initial_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        json = response.json()
        json.pop('id')
        self.assertDictEqual(
            json,
            initial_data
            | {
                'author_sign': None,
                'udc_id': None,
                'bbc_id': None,
                'filename': None,
                'cover': None,
                'federal_book_id': None,
                'tags': None,
                'status': EntryStatus.CURRENT.value,
            },
        )

    def test_create_without_status(self) -> None:
        response = self.client.post(
            self.list_url,
            {
                'author_id': self.author.id,
                'title': 'Математика: 5-й класс: базовый уровень: учебник: в 2 частях',
                'type_id': self.entry_type.id,
                'school_id': self.school.id,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete(self) -> None:
        entry = LibRegistryEntry.objects.create(
            title='Русский язык: 9-й класс: учебник',
            school_id=self.school.id,
            type_id=self.entry_type.id,
            discipline_id=self.discipline.id,
            author=self.author,
        )

        response = self.client.delete(reverse('registry-entries-detail', args=[entry.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(LibRegistryEntry.objects.filter(id=entry.id).first())

    def test_patch(self) -> None:
        author = LibraryAuthors.objects.create(name='Матвеева Н.Б., Ярочкина И.А., Попова М.А. и другие')
        entry_type, _ = LibraryExampleType.objects.get_or_create(id=2, name='Художественная литература')
        bbc, _ = Catalog.objects.get_or_create(id=51, code='36', name='Вычислительная техника')
        udc, _ = LibraryUDC.objects.get_or_create(id=18, code='52', name='Астрономия')
        age_tag, _ = LibMarkInformProduct.objects.get_or_create(id=4, code='16+', name='для детей старше 16 лет')
        discipline = Discipline.objects.create(name='Информатика', id=200)
        school = School.objects.create(id=300, short_name='МОУ СОШ №3', status=True)
        source = LibrarySource.objects.create(name='Муниципальный')
        parallel = Parallel.objects.create(
            title='Параллель 5',
            id=500,
            system_object_id=1,
            object_status=True,
        )
        updated_fields = {
            'type_id': entry_type.id,
            'title': 'Информатика: 9-й класс: учебник: в 2 частях',
            'author_id': author.id,
            'parallel_ids': [parallel.id],
            'author_sign': 'БГ',
            'bbc_id': bbc.id,
            'udc_id': udc.id,
            'tags': 'учебник, 9-й класс',
            'short_info': 'Учебник для 9-го класса',
            'on_balance': False,
            'source_id': source.id,
            'school_id': school.id,
            'discipline_id': discipline.id,
            'age_tag_id': age_tag.id,
            'status': EntryStatus.CURRENT,
        }

        response = self.client.patch(
            reverse('registry-entries-detail', args=[self.entry.id]),
            updated_fields,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            updated_fields
            | {
                'id': self.entry.id,
                'filename': None,
                'cover': None,
                'federal_book_id': None,
                'status': EntryStatus.CURRENT.value,
            },
        )

    def test_patch_with_empty_fields(self) -> None:
        updated_fields = {
            'discipline_id': '',
            'udc_id': '',
            'bbc_id': '',
            'source_id': '',
            'age_tag_id': '',
        }

        response = self.client.patch(
            reverse('registry-entries-detail', args=[self.entry.id]),
            updated_fields,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in updated_fields:
            with self.subTest(field=field):
                self.assertIsNone(response.data[field])

    def test_patch_federal_book(self) -> None:
        publishing = LibraryPublishings.objects.create(name='Вильямс')
        author = LibraryAuthors.objects.create(name='Матвеева Н.Б., Ярочкина И.А., Попова М.А. и другие')
        parallel = Parallel.objects.create(
            title='Параллель 5',
            id=500,
            system_object_id=1,
            object_status=True,
        )
        federal_book = FederalBook.objects.create(
            name='Русский язык: 8-й класс',
            publishing_id=publishing.id,
            author_id=author.id,
            validity_period=timezone.now() + timedelta(days=60),
            pub_lang='русский',
        )
        federal_book.parallel.add(parallel)

        response = self.client.patch(
            reverse('registry-entries-detail', args=[self.entry.id]),
            {'federal_book_id': federal_book.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['federal_book_id'], federal_book.id)
        self.assertEqual(data['title'], federal_book.name)
        self.assertEqual(data['author_id'], federal_book.author_id)
        self.assertEqual(data['parallel_ids'], [parallel.id])

    def test_patch_filename(self) -> None:
        filename = self._create_image()

        response = self.client.patch(
            reverse('registry-entries-detail', args=[self.entry.id]),
            {'filename': filename},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['filename'].endswith(filename.name.split(os.sep)[-1]))

    def test_patch_cover(self) -> None:
        cover = self._create_image()

        response = self.client.patch(
            reverse('registry-entries-detail', args=[self.entry.id]),
            {'cover': cover},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['cover'].endswith('.jpg'))

    def _create_image(self) -> tempfile._TemporaryFileWrapper:
        file = tempfile.NamedTemporaryFile(suffix='.jpg')  # pylint: disable=consider-using-with
        image = Image.new('RGB', (100, 100))
        image.save(file, format='JPEG')
        file.seek(0)

        return file


class GeneralFundTest(BaseEntryTestCase):
    """Тесты реестра общего фонда."""

    def setUp(self) -> None:
        super().setUp()

        self.list_url = reverse('general-fund-list')

    def test_list(self) -> None:
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ('count', 'next', 'previous', 'results'):
            with self.subTest(field=field):
                self.assertIn(field, response.data)
        self.assertDictEqual(
            response.json()['results'][0],
            {
                'id': self.entry.id,
                'municipal_unit': {'id': self.municipal_unit.id, 'name': self.municipal_unit.name},
                'school': {'id': self.school.id, 'name': self.school.name},
                'title': self.entry.title,
                'author': {'id': self.author.id, 'name': self.author.name},
                'type': {'id': self.entry_type.id, 'name': self.entry_type.name},
                'discipline': {'id': self.discipline.id, 'name': self.discipline.name},
                'parallels': [
                    {'id': self.parallel1.id, 'title': self.parallel1.title},
                    {'id': self.parallel2.id, 'title': self.parallel2.title},
                ],
                'editions': '1-е издание, 2-е издание',
                'age_tag': {'id': self.age_tag.id, 'code': self.age_tag.code},
                'publishings': 'Дрофа, Питер',
                'status': EntryStatus.CURRENT.label,
                'publishing_years': '2020, 2024',
                'udc': {'id': self.udc.id, 'name': self.udc.name, 'code': self.udc.code},
                'bbc': {'id': self.bbc.id, 'name': self.bbc.name, 'code': self.bbc.code},
                'federal_book': None,
                'count': 3,
                'free_count': 3,
                'lack': None,
                'excess': 3,
                'sufficiency': 100,
            },
        )

    def test_not_allowed_methods(self) -> None:
        requests = (
            ('post', self.list_url),
        )

        for method, url in requests:
            with self.subTest(method=method):
                response = self.client.generic(method, url)
                self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
