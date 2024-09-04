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
from rest_framework import (
    status,
)
from rest_framework.test import (
    APITransactionTestCase,
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
from edulib.core.lib_registry.domain.model import (
    FinSource,
)
from edulib.core.lib_registry.models import (
    LibRegistryEntry,
    LibRegistryExample,
)
from edulib.core.readers.models import (
    Reader,
)
from edulib.core.schools.models import (
    School,
)


class ExampleRestTests(APITransactionTestCase):
    """Тесты экземпляров библиотечных изданий."""

    @staticmethod
    def create_example(
        entry: LibRegistryEntry,
        publishing: LibraryPublishings,
        **kwargs: Union[str, int, datetime],
    ) -> LibRegistryExample:
        fields = {
            'card_number': '123',
            'lib_reg_entry': entry,
            'edition_year': 2020,
            'edition_place': 'Москва',
            'duration': '200',
            'publishing': publishing,
            'inflow_date': '2020-01-01',
            'book_code': '123',
            'edition': '1-е издание',
            'max_date': '100',
            'fin_source': FinSource.MUNICIPAL,
            'price': 100.54,
            'invoice_number': '1',
        } | kwargs

        return LibRegistryExample.objects.create(**fields)

    def setUp(self) -> None:
        self.school = School.objects.create(id=200, short_name='МОУ СОШ №1', status=True)
        self.author = LibraryAuthors.objects.create(name='Бархударов С.Г., Крючков С.Е., Максимов Л.Ю. и др.')
        self.entry_type, _ = LibraryExampleType.objects.get_or_create(id=1, name='Учебник, учебная литература')
        self.entry = LibRegistryEntry.objects.create(
            title='Русский язык: 8-й класс: учебник',
            school_id=self.school.id,
            type_id=self.entry_type.id,
            author=self.author,
        )
        self.publishing1 = LibraryPublishings.objects.create(name='Дрофа')
        self.publishing2 = LibraryPublishings.objects.create(name='Питер')

        self.example = self.create_example(self.entry, self.publishing1)
        self.example_on_hand = self.create_example(
            self.entry,
            self.publishing2,
            edition_year=2024,
            edition='2-е издание',
            card_number='321',
            invoice_number='2',
        )

        reader = Reader.objects.create()
        IssuanceDelivery.objects.create(
            example=self.example_on_hand,
            issuance_date='2024-03-01',
            fact_delivery_date=timezone.now() + timedelta(days=30),
            reader=reader,
        )

        self.list_url = reverse('examples-list', kwargs={'registryentry_id': self.entry.id})
        self.detail_url = reverse(
            'examples-detail',
            kwargs={'registryentry_id': self.entry.id, 'pk': self.example_on_hand.id},
        )

    def test_list(self) -> None:
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ('count', 'next', 'previous', 'results'):
            with self.subTest(field=field):
                self.assertIn(field, response.data)
        self.assertListEqual(
            response.json()['results'],
            [
                {
                    'id': self.example.id,
                    'card_number': self.example.card_number,
                    'edition': self.example.edition,
                    'edition_year': self.example.edition_year,
                    'inflow_date': self.example.inflow_date,
                    'publishing': {'id': self.publishing1.id, 'name': self.publishing1.name},
                    'occupied': False,
                    'invoice_number': self.example.invoice_number,
                },
                {
                    'id': self.example_on_hand.id,
                    'card_number': self.example_on_hand.card_number,
                    'edition': self.example_on_hand.edition,
                    'edition_year': self.example_on_hand.edition_year,
                    'inflow_date': self.example_on_hand.inflow_date,
                    'publishing': {'id': self.publishing2.id, 'name': self.publishing2.name},
                    'occupied': True,
                    'invoice_number': self.example_on_hand.invoice_number,
                },
            ],
        )

    def test_detail(self) -> None:
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                'id': self.example_on_hand.id,
                'card_number': self.example_on_hand.card_number,
                'edition': self.example_on_hand.edition,
                'edition_year': self.example_on_hand.edition_year,
                'edition_place': self.example_on_hand.edition_place,
                'duration': self.example_on_hand.duration,
                'inflow_date': self.example_on_hand.inflow_date,
                'publishing': {'id': self.publishing2.id, 'name': self.publishing2.name},
                'occupied': True,
                'book_code': self.example_on_hand.book_code,
                'max_date': self.example_on_hand.max_date,
                'fin_source': self.example_on_hand.fin_source.label,
                'price': str(self.example_on_hand.price),
                'invoice_number': self.example_on_hand.invoice_number,
            },
        )

    def test_create(self) -> None:
        initial_data = {
            'invoice_number': '123',
            'inflow_date': '2024-03-01',
            'edition_place': 'Москва',
            'edition_year': 2020,
            'duration': '200',
            'book_code': '22.1 B-57',
            'publishing_id': self.publishing1.id,
            'fin_source': FinSource.SPONSOR,
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
                'card_number': None,
                'edition': None,
                'max_date': None,
                'price': None,
                'fin_source': initial_data['fin_source'].value,
            },
        )

    def test_patch(self) -> None:
        updated_fields = {
            'card_number': '2024-004',
            'invoice_number': '234',
            'inflow_date': '2024-04-01',
            'edition': '3-е издание',
            'edition_place': 'Санкт-Петербург',
            'edition_year': 2021,
            'duration': '250',
            'book_code': '22.1 B-68',
            'max_date': '150',
            'price': '200.55',
            'fin_source': FinSource.REGIONAL,
            'publishing_id': self.publishing1.id,
        }

        response = self.client.patch(self.detail_url, updated_fields)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            updated_fields
            | {
                'id': self.example_on_hand.id,
            },
        )

    def test_delete(self) -> None:
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(LibRegistryExample.objects.filter(id=self.example_on_hand.id).first())

    def test_copy(self) -> None:
        self.assertEqual(LibRegistryExample.objects.filter(lib_reg_entry_id=self.entry.id).count(), 2)

        response = self.client.post(
            reverse('examples-copy', kwargs={'registryentry_id': self.entry.id, 'pk': self.example_on_hand.id}),
            {'count_for_copy': 2},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LibRegistryExample.objects.filter(lib_reg_entry_id=self.entry.id).count(), 4)
