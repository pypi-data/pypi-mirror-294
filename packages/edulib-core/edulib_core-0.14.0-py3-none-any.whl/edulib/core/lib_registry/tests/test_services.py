from datetime import (
    date,
    datetime,
    timedelta,
)
from typing import (
    Any,
    Union,
)

from django.test import (
    TransactionTestCase,
)
from django.utils import (
    timezone,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
)

from edulib.core import (
    bus,
)
from edulib.core.directory.models import (
    Catalog,
)
from edulib.core.disciplines.domain import (
    Discipline,
)
from edulib.core.federal_books.domain import (
    FederalBook,
)
from edulib.core.lib_authors.domain import (
    Author,
)
from edulib.core.lib_example_types.domain import (
    ExampleType,
)
from edulib.core.lib_example_types.models import (
    LibraryExampleType,
)
from edulib.core.lib_publishings.domain import (
    Publishing,
)
from edulib.core.lib_registry.domain import (
    CopyRegistryExample,
    CreateRegistryEntry,
    CreateRegistryExample,
    DeleteRegistryEntry,
    DeleteRegistryExample,
    EntryStatus,
    RegistryEntry,
    RegistryEntryNotFound,
    RegistryExample,
    RegistryExampleNotFound,
    UpdateRegistryEntry,
    UpdateRegistryExample,
)
from edulib.core.lib_registry.models import (
    LibMarkInformProduct,
    LibRegistryExample,
)
from edulib.core.lib_sources.domain import (
    Source,
)
from edulib.core.lib_udc.models import (
    LibraryUDC,
)
from edulib.core.parallels.domain import (
    Parallel,
)
from edulib.core.schools.domain import (
    School,
)


class RegistryEntryTestCase(TransactionTestCase):
    @classmethod
    def setUpClass(cls: 'RegistryEntryTestCase') -> None:
        super().setUpClass()

        cls.repository = bus.get_uow().registry_entries

    def setUp(self) -> None:
        entry_type, _ = LibraryExampleType.objects.get_or_create(id=1, name='Учебник, учебная литература')
        bbc, _ = Catalog.objects.get_or_create(id=103, code='86.7', name='Свободомыслие')
        udc, _ = LibraryUDC.objects.get_or_create(id=10, code='8', name='Языкознание')
        age_tag, _ = LibMarkInformProduct.objects.get_or_create(id=3, code='12+', name='для детей старше 12 лет')

        author = bus.get_uow().authors.add(Author(name='Бархударов С.Г., Крючков С.Е., Максимов Л.Ю. и др.'))
        discipline = bus.get_uow().disciplines.add(Discipline(id=100, name='Русский язык'))
        school = bus.get_uow().schools.add(School(id=200, short_name='МОУ СОШ №1', status=True))
        source = bus.get_uow().sources.add(Source(name='Федеральный'))
        parallel = bus.get_uow().parallels.add(
            Parallel(id=300, title='Параллель 1', object_status=True, system_object_id=1),
        )

        self.registry_entry = {
            'type_id': entry_type.id,
            'title': 'Русский язык: 8-й класс: учебник',
            'author_id': author.id,
            'parallel_ids': [parallel.id],
            'author_sign': 'БС',
            'bbc_id': bbc.id,
            'udc_id': udc.id,
            'tags': 'учебник, 8-й класс',
            'source_id': source.id,
            'short_info': 'Учебник для школьников',
            'on_balance': True,
            'school_id': school.id,
            'discipline_id': discipline.id,
            'age_tag_id': age_tag.id,
            'status': EntryStatus.DISCARDED,
        }

    def _create_federal_book(self, **kwargs: Union[str, int]) -> FederalBook:
        publishing = bus.get_uow().publishings.add(Publishing(name='Дрофа'))
        author = bus.get_uow().authors.add(Author(name='Бархударов С.Г. и др.'))
        parallel = bus.get_uow().parallels.add(
            Parallel(id=200, title='Параллель 2', object_status=True, system_object_id=2),
        )
        fields = {
            'name': 'Русский язык: 8-й класс',
            'publishing_id': publishing.id,
            'authors': author.id,
            'validity_period': timezone.now() + timedelta(days=60),
            'pub_lang': 'русский',
            'parallel_ids': [parallel.id],
        } | kwargs

        return bus.get_uow().federal_books.add(FederalBook(**fields))

    def test_create_registry_entry(self) -> None:
        """Тест создания библиотечного издания."""
        command = CreateRegistryEntry(**self.registry_entry)

        registry_entry = bus.handle(command)

        self.assertIsNotNone(registry_entry.id)
        db_registry_entry = bus.get_uow().registry_entries.get_object_by_id(registry_entry.id)
        for field, value in self.registry_entry.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(registry_entry, field), value)
                self.assertEqual(getattr(db_registry_entry, field), value)

    def test_create_registry_entry_with_federal_book_id(self) -> None:
        """Тест создания издания с указанием учебника федерального справочника."""
        federal_book = self._create_federal_book()
        command = CreateRegistryEntry(**self.registry_entry | {'federal_book_id': federal_book.id})

        registry_entry = bus.handle(command)

        self.assertEqual(
            bus.get_uow().registry_entries.get_object_by_id(registry_entry.id).federal_book_id, federal_book.id
        )
        self.assertEqual(registry_entry.federal_book_id, federal_book.id)
        self.assertEqual(registry_entry.title, federal_book.name)
        self.assertEqual(registry_entry.author_id, federal_book.authors)
        self.assertEqual(registry_entry.parallel_ids, federal_book.parallel_ids)

    def test_create_registry_entry_with_federal_book_id_and_mismatching_type(self) -> None:
        """Тест создания издания с указанием учебника федерального справочника с некорректным типом."""
        federal_book = self._create_federal_book()
        entry_type = bus.get_uow().example_types.add(ExampleType(name='Нехудожественная литература'))
        command = CreateRegistryEntry(
            **self.registry_entry | {'type_id': entry_type.id, 'federal_book_id': federal_book.id}
        )

        with self.assertRaises(DomainValidationError) as exc:
            bus.handle(command)
        self.assertIn(
            (
                'Учебник федерального перечня может быть указан только для '
                'типа библиотечного издания "Учебник, учебная литература"'
            ),
            exc.exception.messages,
        )

    def test_failed_commands(self) -> None:
        """Тест неудавшихся команд."""
        federal_book = self._create_federal_book()
        registry_entry = self.repository.add(
            RegistryEntry(**self.registry_entry | {'title': federal_book.name, 'author_id': federal_book.authors})
        )
        commands_with_errors = (
            (
                CreateRegistryEntry(**self.registry_entry | {'federal_book_id': federal_book.id}),
                '__root__',
                'Такое библиотечное издание уже существует',
            ),
            (
                CreateRegistryEntry(
                    **self.registry_entry | {'title': federal_book.name, 'author_id': federal_book.authors}
                ),
                '__root__',
                'Такое библиотечное издание уже существует',
            ),
            (CreateRegistryEntry(**self.registry_entry | {'bbc_id': 10_000}), 'bbc_id', 'Раздел ББК не найден'),
            (UpdateRegistryEntry(id=registry_entry.id, bbc_id=10_000), 'bbc_id', 'Раздел ББК не найден'),
            (CreateRegistryEntry(**self.registry_entry | {'udc_id': 10_000}), 'udc_id', 'Раздел УДК не найден'),
            (UpdateRegistryEntry(id=registry_entry.id, udc_id=10_000), 'udc_id', 'Раздел УДК не найден'),
            (
                CreateRegistryEntry(**{key: value for key, value in self.registry_entry.items() if key != 'author_id'}),
                '__root__',
                'Необходимо указать наименование и автора, либо учебник федерального перечня',
            ),
            (
                UpdateRegistryEntry(id=registry_entry.id, author_id=None),
                '__root__',
                'Необходимо указать наименование и автора, либо учебник федерального перечня',
            ),
            (
                CreateRegistryEntry(**{key: value for key, value in self.registry_entry.items() if key != 'title'}),
                '__root__',
                'Необходимо указать наименование и автора, либо учебник федерального перечня',
            ),
            (
                UpdateRegistryEntry(id=registry_entry.id, title=None),
                '__root__',
                'Необходимо указать наименование и автора, либо учебник федерального перечня',
            ),
            (
                CreateRegistryEntry(**self.registry_entry | {'discipline_id': 10_000}),
                'discipline_id',
                'Предмет не найден',
            ),
            (
                UpdateRegistryEntry(id=registry_entry.id, discipline_id=10_000),
                'discipline_id',
                'Предмет не найден',
            ),
            (
                CreateRegistryEntry(**self.registry_entry | {'type_id': 10_000}),
                'type_id',
                'Тип библиотечных экземпляров не найден',
            ),
            (
                UpdateRegistryEntry(id=registry_entry.id, type_id=10_000),
                'type_id',
                'Тип библиотечных экземпляров не найден',
            ),
            (
                CreateRegistryEntry(**self.registry_entry | {'author_id': 10_000}),
                'author_id',
                'Автор не найден',
            ),
            (
                UpdateRegistryEntry(id=registry_entry.id, author_id=10_000),
                'author_id',
                'Автор не найден',
            ),
            (
                CreateRegistryEntry(**self.registry_entry | {'source_id': 10_000}),
                'source_id',
                'Источник поступления в библиотеку не найден',
            ),
            (
                UpdateRegistryEntry(id=registry_entry.id, source_id=10_000),
                'source_id',
                'Источник поступления в библиотеку не найден',
            ),
            (
                UpdateRegistryEntry(id=registry_entry.id, source_id=0),
                'source_id',
                'Источник поступления в библиотеку не найден',
            ),
            (
                CreateRegistryEntry(**self.registry_entry | {'age_tag_id': 10_000}),
                'age_tag_id',
                'Знак информационной продукции не найден',
            ),
            (
                UpdateRegistryEntry(id=registry_entry.id, age_tag_id=10_000),
                'age_tag_id',
                'Знак информационной продукции не найден',
            ),
            (
                CreateRegistryEntry(**self.registry_entry | {'school_id': 10_000}),
                'school_id',
                'Образовательная организация не найдена',
            ),
            (
                UpdateRegistryEntry(id=registry_entry.id, school_id=10_000),
                'school_id',
                'Образовательная организация не найдена',
            ),
            (
                CreateRegistryEntry(**self.registry_entry | {'parallel_ids': [10_000]}),
                'parallel_ids',
                'Не найдены параллели с ID: 10000',
            ),
            (
                UpdateRegistryEntry(id=registry_entry.id, parallel_ids=[10_100]),
                'parallel_ids',
                'Не найдены параллели с ID: 10100',
            ),
            (
                CreateRegistryEntry(**self.registry_entry | {'federal_book_id': 10_000}),
                'federal_book_id',
                'Учебник из Федерального перечня учебников не найден',
            ),
            (
                UpdateRegistryEntry(id=registry_entry.id, federal_book_id=10_000),
                'federal_book_id',
                'Учебник из Федерального перечня учебников не найден',
            ),
            (UpdateRegistryEntry(id=10_000, title='Учебник'), 'id', 'Библиотечное издание не найдено'),
            (DeleteRegistryEntry(id=10_000), 'id', 'Библиотечное издание не найдено'),
        )

        for command, error, message in commands_with_errors:
            with self.subTest(message=message, command=command):
                with self.assertRaises(DomainValidationError) as exc:
                    bus.handle(command)
                self.assertIn(message, exc.exception.message_dict[error])

    def test_update_registry_entry(self) -> None:
        """Тест обновления библиотечного издания."""
        registry_entry = self.repository.add(RegistryEntry(**self.registry_entry))
        author = bus.get_uow().authors.add(Author(name='Матвеева Н.Б., Ярочкина И.А., Попова М.А. и другие'))
        entry_type, _ = LibraryExampleType.objects.get_or_create(id=2, name='Художественная литература')
        bbc, _ = Catalog.objects.get_or_create(id=51, code='36', name='Вычислительная техника')
        udc, _ = LibraryUDC.objects.get_or_create(id=18, code='52', name='Астрономия')
        age_tag, _ = LibMarkInformProduct.objects.get_or_create(id=4, code='16+', name='для детей старше 16 лет')
        discipline = bus.get_uow().disciplines.add(Discipline(id=150, name='Литература'))
        school = bus.get_uow().schools.add(School(id=300, short_name='МОУ СОШ №2', status=True))
        source = bus.get_uow().sources.add(Source(name='Муниципальный'))
        parallel = bus.get_uow().parallels.add(
            Parallel(id=400, title='Параллель 7', object_status=True, system_object_id=2),
        )
        updated_fields = {
            'type_id': entry_type.id,
            'title': 'Информатика',
            'author_id': author.id,
            'parallel_ids': [parallel.id],
            'author_sign': 'БГ',
            'bbc_id': bbc.id,
            'udc_id': udc.id,
            'tags': 'учебник, 10-й класс',
            'short_info': 'Учебник для 10-го класса',
            'on_balance': False,
            'source_id': source.id,
            'school_id': school.id,
            'discipline_id': discipline.id,
            'age_tag_id': age_tag.id,
            'status': EntryStatus.CURRENT,
        }

        registry_entry = bus.handle(UpdateRegistryEntry(id=registry_entry.id, **updated_fields))

        db_registry_entry = self.repository.get_object_by_id(registry_entry.id)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(registry_entry, field), value)
                self.assertEqual(getattr(db_registry_entry, field), value)

    def test_update_federal_book_for_registry_entry(self) -> None:
        """Тест обновления учебника федерального перечня у библиотечного издания."""
        federal_book = self._create_federal_book()
        registry_entry = self.repository.add(RegistryEntry(**self.registry_entry))
        command = UpdateRegistryEntry(id=registry_entry.id, federal_book_id=federal_book.id)

        registry_entry = bus.handle(command)

        self.assertEqual(registry_entry.author_id, federal_book.authors)
        self.assertEqual(registry_entry.title, federal_book.name)
        self.assertEqual(registry_entry.parallel_ids, federal_book.parallel_ids)

    def test_update_type_for_registry_entry_with_federal_book(self) -> None:
        """Тест обновления типа у библиотечного издания из федерального перечня."""
        federal_book = self._create_federal_book()
        registry_entry = self.repository.add(
            RegistryEntry(
                **self.registry_entry
                | {
                    'title': federal_book.name,
                    'author_id': federal_book.authors,
                    'parallel_ids': federal_book.parallel_ids,
                    'federal_book_id': federal_book.id,
                }
            )
        )
        entry_type, _ = LibraryExampleType.objects.get_or_create(id=2, name='Художественная литература')
        command = UpdateRegistryEntry(id=registry_entry.id, type_id=entry_type.id)

        with self.assertRaises(DomainValidationError) as exc:
            bus.handle(command)
        self.assertIn(
            (
                'Учебник федерального перечня может быть указан только для '
                'типа библиотечного издания "Учебник, учебная литература"'
            ),
            exc.exception.messages,
        )
        self.assertEqual(self.repository.get_object_by_id(registry_entry.id).type_id, self.registry_entry['type_id'])

    def test_update_title_that_matches_another(self) -> None:
        """Тест обновления наименования библиотечного издания совпадающего с другим."""
        self.repository.add(RegistryEntry(**self.registry_entry))
        registry_entry = self.repository.add(RegistryEntry(**self.registry_entry | {'title': 'Русский язык'}))
        command = UpdateRegistryEntry(id=registry_entry.id, title=self.registry_entry['title'])

        with self.assertRaises(DomainValidationError) as exc:
            bus.handle(command)
        self.assertIn('Такое библиотечное издание уже существует', exc.exception.messages)

    def test_update_author_that_matches_another(self) -> None:
        """Тест обновления автора библиотечного издания совпадающего с другим."""
        self.repository.add(RegistryEntry(**self.registry_entry))
        author = bus.get_uow().authors.add(Author(name='Бархударов С.Г. и др.'))
        registry_entry = self.repository.add(RegistryEntry(**self.registry_entry | {'author_id': author.id}))
        command = UpdateRegistryEntry(id=registry_entry.id, author_id=self.registry_entry['author_id'])

        with self.assertRaises(DomainValidationError) as exc:
            bus.handle(command)
        self.assertIn('Такое библиотечное издание уже существует', exc.exception.messages)

    def test_delete_registry_entry(self) -> None:
        """Тест удаления библиотечного издания."""
        registry_entry = self.repository.add(RegistryEntry(**self.registry_entry))
        command = DeleteRegistryEntry(id=registry_entry.id)

        bus.handle(command)

        with self.assertRaises(RegistryEntryNotFound):
            self.repository.get_object_by_id(registry_entry.id)

    def test_delete_registry_entry_with_examples(self) -> None:
        """Тест удаления библиотечного издания с экземплярами."""
        registry_entry = self.repository.add(RegistryEntry(**self.registry_entry))
        publishing = bus.get_uow().publishings.add(Publishing(name='Дрофа'))
        LibRegistryExample.objects.create(
            lib_reg_entry_id=registry_entry.id,
            publishing_id=publishing.id,
            inflow_date='2024-03-01',
            edition_place='Москва',
            edition_year=2024,
            duration=200,
            book_code='123',
            invoice_number='1',
        )

        with self.assertRaises(DomainValidationError) as exc:
            bus.handle(DeleteRegistryEntry(id=registry_entry.id))
        self.assertIn('Невозможно удалить библиотечное издание, т.к. имеются экземпляры', exc.exception.messages)
        self.assertIsNotNone(self.repository.get_object_by_id(registry_entry.id))


class RegistryExampleTestCase(TransactionTestCase):
    @classmethod
    def setUpClass(cls: 'RegistryExampleTestCase') -> None:
        super().setUpClass()

        cls.uow = bus.get_uow()

    def setUp(self) -> None:
        registry_entry = self._create_registry_entry()
        publishing = self.uow.publishings.add(Publishing(name='Дрофа'))
        self.registry_example = {
            'lib_reg_entry_id': registry_entry.id,
            'invoice_number': '123',
            'inflow_date': date(2024, 3, 1),
            'edition_place': 'Москва',
            'edition_year': 2020,
            'duration': '200',
            'book_code': '22.1 B-57',
            'publishing_id': publishing.id,
        }

    def test_create_registry_example(self) -> None:
        """Тест создания экземпляра библиотечного издания."""
        registry_example = bus.handle(CreateRegistryExample(**self.registry_example))

        self.assertIsNotNone(registry_example.id)
        db_registry_example = self.uow.registry_examples.get_object_by_id(registry_example.id)
        for field, value in self.registry_example.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(db_registry_example, field), value)
                self.assertEqual(getattr(registry_example, field), value)

    def test_update_registry_example(self) -> None:
        """Тест обновления экземпляра библиотечного издания."""
        registry_example = self.uow.registry_examples.add(RegistryExample(**self.registry_example))
        publishing = self.uow.publishings.add(Publishing(name='Питер'))
        updated_fields = {
            'card_number': '2024-004',
            'invoice_number': '234',
            'inflow_date': date(2024, 4, 1),
            'edition_place': 'Санкт-Петербург',
            'edition_year': 2021,
            'duration': '250',
            'book_code': '22.1 B-68',
            'publishing_id': publishing.id,
        }

        registry_example = bus.handle(UpdateRegistryExample(id=registry_example.id, **updated_fields))

        db_registry_example = self.uow.registry_examples.get_object_by_id(registry_example.id)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(db_registry_example, field), value)
                self.assertEqual(getattr(registry_example, field), value)

    def test_failed_commands(self) -> None:
        """Тест неудавшихся команд."""
        registry_example = self.uow.registry_examples.add(RegistryExample(**self.registry_example))
        commands_with_errors = (
            (
                CreateRegistryExample(**self.registry_example | {'lib_reg_entry_id': 10_000}),
                'lib_reg_entry_id',
                'Библиотечное издание не найдено',
            ),
            (
                CreateRegistryExample(**self.registry_example | {'publishing_id': 10_000}),
                'publishing_id',
                'Издательство не найдено',
            ),
            (
                UpdateRegistryExample(id=registry_example.id, publishing_id=10_000),
                'publishing_id',
                'Издательство не найдено',
            ),
            (
                UpdateRegistryExample(id=10_000, card_number='2024-004'),
                'id',
                'Экземпляр библиотечного издания не найден',
            ),
            (
                CopyRegistryExample(id=10_000, count_for_copy=2),
                'id',
                'Экземпляр библиотечного издания не найден',
            ),
            (DeleteRegistryExample(id=10_000), 'id', 'Экземпляр библиотечного издания не найден'),
        )

        for command, error, message in commands_with_errors:
            with self.subTest(message=message, command=command):
                with self.assertRaises(DomainValidationError) as exc:
                    bus.handle(command)
                self.assertIn(message, exc.exception.message_dict[error])

    def test_delete_registry_example(self) -> None:
        """Тест удаления экземпляра библиотечного издания."""
        registry_example = self.uow.registry_examples.add(RegistryExample(**self.registry_example))
        command = DeleteRegistryExample(id=registry_example.id)

        bus.handle(command)

        with self.assertRaises(RegistryExampleNotFound):
            self.uow.registry_examples.get_object_by_id(registry_example.id)

    def test_copy_registry_example(self) -> None:
        """Тест копирования экземпляра библиотечного издания."""
        registry_example = self.uow.registry_examples.add(RegistryExample(**self.registry_example))
        command = CopyRegistryExample(id=registry_example.id, count_for_copy=1)
        current_year = datetime.now().year

        bus.handle(command)

        copy = LibRegistryExample.objects.filter(
            lib_reg_entry_id=registry_example.lib_reg_entry_id,
        ).exclude(id=registry_example.id).first()
        self.assertEqual(copy.card_number, f'{current_year}-002')

    def _create_registry_entry(self, **kwargs: Any) -> RegistryEntry:
        if kwargs.get('author_id'):
            author_id = kwargs.pop('author_id')
        else:
            author_id = self.uow.authors.add(Author(name='Бархударов С.Г., Крючков С.Е., Максимов Л.Ю. и др.')).id

        entry_type, _ = LibraryExampleType.objects.get_or_create(id=1, name='Учебник, учебная литература')
        school = self.uow.schools.add(School(id=200, short_name='МОУ СОШ №1', status=True))
        fields = {
            'type_id': entry_type.id,
            'title': 'Русский язык: 8-й класс: учебник',
            'author_id': author_id,
            'on_balance': True,
            'school_id': school.id,
            'status': EntryStatus.CURRENT,
        } | kwargs

        return self.uow.registry_entries.add(RegistryEntry(**fields))
