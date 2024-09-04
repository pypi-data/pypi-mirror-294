from django.test import (
    TransactionTestCase,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
)

from edulib.core import (
    bus,
)
from edulib.core.lib_registry.tests.utils import (
    get_registry_entry,
)
from edulib.core.lib_sources.adapters.db import (
    repository,
)
from edulib.core.lib_sources.domain.commands import (
    CreateSource,
    DeleteSource,
    UpdateSource,
)
from edulib.core.lib_sources.domain.model import (
    Source,
    SourceNotFound,
)


class SourceTestCase(TransactionTestCase):

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.source = {
            'name': 'Федеральный бюджет',
        }

    def test_create_source(self) -> None:
        """Тест создания источника поступления."""
        command = CreateSource(**self.source)

        source = bus.handle(command)

        self.assertIsNotNone(source.id)
        db_source = repository.get_object_by_id(source.id)
        for field, value in self.source.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(source, field), value)
                self.assertEqual(getattr(db_source, field), value)

    def test_update_source(self) -> None:
        """Тест изменения источника поступления."""
        source = repository.add(Source(**self.source))
        updated_fields = {
            'name': 'Муниципальный бюджет',
        }
        command = UpdateSource(id=source.id, **updated_fields)

        result = bus.handle(command)

        db_source = repository.get_object_by_id(source.id)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(result, field), value)
                self.assertEqual(getattr(db_source, field), value)

    def test_delete_source(self) -> None:
        """Тест удаления источника поступления."""
        source = repository.add(Source(**self.source))
        command = DeleteSource(id=source.id)

        bus.handle(command)

        with self.assertRaises(SourceNotFound):
            repository.get_object_by_id(source.id)

    def test_delete_linked_source(self) -> None:
        source = repository.add(Source(**self.source))
        get_registry_entry(bus.get_uow(), source_id=source.id)
        command = DeleteSource(id=source.id)

        with self.assertRaises(DomainValidationError) as exc:
            bus.handle(command)
        self.assertIn(
            f'Источник поступления "{source.name}" связан с библиотечными изданиями и не может быть удален',
            exc.exception.message_dict['id']
        )

    def test_source_not_found(self) -> None:
        """Тест источника поступления, который не удалось найти."""
        command = UpdateSource(id=1, name='Издательство Питер')

        with self.assertRaises(DomainValidationError) as exc:
            bus.handle(command)

            self.assertIn('Источник поступления в библиотеку не найден', exc.exception.message_dict['id'])

    def test_failed_commands(self) -> None:
        """Тест неудавшихся команд."""
        source = repository.add(Source(**self.source))
        commands_with_errors = (
            (CreateSource(**self.source),
             f'Источник поступления с именем "{source.name}" уже существует'),
            (CreateSource(name='', school_id=1), 'Наименование не может быть пустым'),
            (UpdateSource(id=source.id, name='', school_id=1), 'Наименование не может быть пустым'),
        )

        for command, error in commands_with_errors:
            with self.subTest(command=command):
                with self.assertRaises(DomainValidationError) as err:
                    bus.handle(command)

                self.assertIn(error, err.exception.message_dict['name'])
