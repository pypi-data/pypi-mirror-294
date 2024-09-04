from django.test import (
    TransactionTestCase,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
)

from edulib.core import (
    bus,
)
from edulib.core.lib_udc.domain.commands import (
    CreateUdc,
    DeleteUdc,
    UpdateUdc,
)
from edulib.core.lib_udc.domain.model import (
    Udc,
    UdcNotFound,
)


class UdcTestCase(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        cls.repository = bus.get_uow().udc

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.udc = {
            'code': '621.396.677.41',
            'name': 'Бевериджа антенны',
        }

    def test_create_udc(self) -> None:
        """Тест создания раздела УДК."""
        command = CreateUdc(**self.udc)

        udc = bus.handle(command)

        self.assertIsNotNone(udc.id)
        db_udc = self.repository.get_object_by_id(udc.id)
        for field, value in self.udc.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(udc, field), value)
                self.assertEqual(getattr(db_udc, field), value)

    def test_update_udc(self) -> None:
        """Тест обновления раздела УДК."""
        udc = self.repository.add(Udc(**self.udc))
        updated_fields = {
            'code': '621.396.677.4',
            'name': 'Волновые антенны',
        }
        command = UpdateUdc(id=udc.id, **updated_fields)

        result = bus.handle(command)

        db_udc = self.repository.get_object_by_id(udc.id)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(result, field), value)
                self.assertEqual(getattr(db_udc, field), value)

    def test_delete_udc(self) -> None:
        """Тест удаления раздела УДК."""
        udc = self.repository.add(Udc(**self.udc))
        command = DeleteUdc(id=udc.id)

        bus.handle(command)

        with self.assertRaises(UdcNotFound):
            self.repository.get_object_by_id(udc.id)

    def test_failed_commands(self) -> None:
        """Тест неудавшихся команд."""
        udc = self.repository.add(Udc(**self.udc))
        commands_with_errors = (
            (CreateUdc(**self.udc), 'code', 'Такой раздел УДК уже существует'),
            (CreateUdc(code='621.396.677.4', name=''), 'name', 'Наименование не может быть пустым'),
            (CreateUdc(code='', name='Волновые антенны'), 'code', 'Код не может быть пустым'),
            (UpdateUdc(id=udc.id, name=''), 'name', 'Наименование не может быть пустым'),
            (UpdateUdc(id=udc.id, code=''), 'code', 'Код не может быть пустым'),
            (UpdateUdc(id=10_000, code='621.396.677.4'), 'id', 'Раздел УДК не найден'),
            (
                CreateUdc(code='621.396.677.4', name='Волновые антенны', parent_id=10_000),
                'parent_id',
                'Раздел УДК не найден',
            ),
            (DeleteUdc(id=10_000), 'id', 'Раздел УДК не найден'),
        )

        for command, error, message in commands_with_errors:
            with self.subTest(command=command):
                with self.assertRaises(DomainValidationError) as exc:
                    bus.handle(command)

                self.assertIn(message, exc.exception.message_dict[error])
