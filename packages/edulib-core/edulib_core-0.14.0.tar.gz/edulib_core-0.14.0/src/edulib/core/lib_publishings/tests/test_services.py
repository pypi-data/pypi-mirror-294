from django.test import (
    TransactionTestCase,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
)

from edulib.core import (
    bus,
)
from edulib.core.lib_authors.domain import (
    Author,
)
from edulib.core.lib_example_types.models import (
    LibraryExampleType,
)
from edulib.core.lib_publishings.adapters.db import (
    repository,
)
from edulib.core.lib_publishings.domain.commands import (
    CreatePublishing,
    DeletePublishing,
    UpdatePublishing,
)
from edulib.core.lib_publishings.domain.model import (
    Publishing,
    PublishingNotFound,
)
from edulib.core.lib_registry.domain import (
    RegistryEntry,
)
from edulib.core.lib_registry.models import (
    LibRegistryExample,
)
from edulib.core.schools.domain import (
    School,
)


class PublishingTestCase(TransactionTestCase):

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.publishing = {
            'name': 'Питер',
        }

    def test_create_publishing(self) -> None:
        """Тест создания издательства."""
        command = CreatePublishing(**self.publishing)

        publishing = bus.handle(command)

        self.assertIsNotNone(publishing.id)
        db_publishing = repository.get_object_by_id(publishing.id)
        for field, value in self.publishing.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(publishing, field), value)
                self.assertEqual(getattr(db_publishing, field), value)

    def test_update_publishing(self) -> None:
        """Тест обновления издательства."""
        publishing = repository.add(Publishing(**self.publishing))
        updated_fields = {
            'name': 'БХВ',
        }
        command = UpdatePublishing(id=publishing.id, **updated_fields)

        result = bus.handle(command)

        db_publishing = repository.get_object_by_id(publishing.id)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(result, field), value)
                self.assertEqual(getattr(db_publishing, field), value)

    def test_delete_publishing(self) -> None:
        """Тест удаления издательства."""
        publishing = repository.add(Publishing(**self.publishing))
        command = DeletePublishing(id=publishing.id)

        bus.handle(command)

        with self.assertRaises(PublishingNotFound):
            repository.get_object_by_id(publishing.id)

    def test_delete_publishing_with_examples(self) -> None:
        """Тест удаления издательства с экземплярами."""
        entry_type, _ = LibraryExampleType.objects.get_or_create(id=1, name='Учебник, учебная литература')
        school = bus.get_uow().schools.add(School(id=200, short_name='МОУ СОШ №1', status=True))
        author = bus.get_uow().authors.add(Author(name='Бархударов С.Г., Крючков С.Е., Максимов Л.Ю. и др.'))
        publishing = bus.get_uow().publishings.add(Publishing(name='Дрофа'))
        registry_entry = bus.get_uow().registry_entries.add(RegistryEntry(
            title='Русский язык: 8-й класс: учебник',
            author_id=author.id,
            school_id=school.id,
            type_id=entry_type.id,
        ))
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
            bus.handle(DeletePublishing(id=publishing.id))
        self.assertIn('Невозможно удалить издательство, т.к. имеются экземпляры', exc.exception.messages)

    def test_failed_commands(self) -> None:
        """Тест неудавшихся команд."""
        publishing = repository.add(Publishing(**self.publishing))
        commands_with_errors = (
            (CreatePublishing(**self.publishing), 'name', 'Такое издательство уже существует'),
            (CreatePublishing(name=''), 'name', 'Издательство не может быть пустым'),
            (UpdatePublishing(id=publishing.id, name=''), 'name', 'Издательство не может быть пустым'),
            (UpdatePublishing(id=10_000, name='Дрофа'), 'id', 'Издательство не найдено'),
            (DeletePublishing(id=10_000), 'id', 'Издательство не найдено'),
        )

        for command, error, message in commands_with_errors:
            with self.subTest(command=command):
                with self.assertRaises(DomainValidationError) as err:
                    bus.handle(command)

                self.assertIn(message, err.exception.message_dict[error])
