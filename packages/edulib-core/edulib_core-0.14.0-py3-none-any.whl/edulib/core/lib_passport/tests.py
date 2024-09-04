from django.test import (
    TransactionTestCase,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
)

from edulib.core import (
    bus,
)
from edulib.core.base.tests.utils import (
    randint,
)
from edulib.core.lib_passport.adapters.db import (
    passport_repository,
    work_mode_repository,
)
from edulib.core.lib_passport.domain import (
    CreatePassport,
    CreateWorkMode,
    DeletePassport,
    DeleteWorkMode,
    UpdatePassport,
    UpdateWorkMode,
)
from edulib.core.lib_passport.domain.model import (
    Passport,
    PassportNotFound,
    WorkMode,
    WorkModeNotFound,
)
from edulib.core.schools import (
    domain as schools,
)
from edulib.core.schools.adapters.db import (
    repository as school_repo,
)


class PassportTestCase(TransactionTestCase):

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.school = school_repo.add(schools.School(short_name='Школа №1', id=4815162342, status=True))
        self.passport = {
            'name': 'Библиотека имени В.В. Маяковского',
            'school_id': self.school.id,
        }

    def test_create_passport(self) -> None:
        """Тест создания паспорта библиотеки."""
        command = CreatePassport(**self.passport)

        passport = bus.handle(command)

        self.assertIsNotNone(passport.id)
        db_passport = passport_repository.get_object_by_id(passport.id)
        for field, value in self.passport.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(passport, field), value)
                self.assertEqual(getattr(db_passport, field), value)

    def test_update_passport(self) -> None:
        """Тест обновления паспорта библиотеки."""
        passport = passport_repository.add(Passport(**self.passport))
        updated_fields = {
            'name': 'Библиотека имени Есенина',
        }
        command = UpdatePassport(id=passport.id, **updated_fields)

        result = bus.handle(command)

        db_passport = passport_repository.get_object_by_id(passport.id)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(result, field), value)
                self.assertEqual(getattr(db_passport, field), value)

    def test_delete_passport(self) -> None:
        """Тест удаления паспорта библиотеки."""
        passport = passport_repository.add(Passport(**self.passport))
        command = DeletePassport(id=passport.id)

        bus.handle(command)

        with self.assertRaises(PassportNotFound):
            passport_repository.get_object_by_id(passport.id)

    def test_failed_commands(self) -> None:
        """Тест неудавшихся команд."""
        passport_repository.add(Passport(**self.passport))
        commands_with_errors = (
            (CreatePassport(**self.passport), 'name', 'Такой паспорт библиотеки уже существует'),
            (CreatePassport(name='', school_id=self.school.id), 'name', 'Наименование библиотеки не может быть пустым'),
            (UpdatePassport(id=10_000, ), 'id', 'Паспорт библиотеки не найден'),
            (DeletePassport(id=10_000), 'id', 'Паспорт библиотеки не найден'),
        )

        for command, error, message in commands_with_errors:
            with self.subTest(command=command):
                with self.assertRaises(DomainValidationError) as exc:
                    bus.handle(command)

                self.assertIn(message, exc.exception.message_dict[error])


class DefaultPassportsTestCase(TransactionTestCase):

    def test_create_passport_on_school_created(self):
        """Проверка создания паспорта при создании организации."""
        school_id = randint()
        bus.handle(schools.SchoolCreated(
            id=school_id, short_name='МБОУ СОШ 13', status=True
        ))

        school = bus.get_uow().schools.get_object_by_id(school_id)
        passport = bus.get_uow().passports.get_by_school_id(school_id)

        self.assertEqual(passport.name, school.short_name)

    def test_create_passport_on_school_updated(self):
        """Проверка создания паспорта при обновлении организации без паспорта.

        На случай, если в Kafka нет события создания организации.
        """
        school_id = randint()

        # Через репо, чтобы не стриггерить создание паспорта
        bus.get_uow().schools.add(schools.School(id=school_id, short_name='МБОУ СОШ 13', status=True))

        with self.assertRaises(PassportNotFound):  # Самопроверка
            bus.get_uow().passports.get_by_school_id(school_id)

        bus.handle(schools.SchoolUpdated(id=school_id, short_name='МБОУ СОШ 14'))

        school = bus.get_uow().schools.get_object_by_id(school_id)
        passport = bus.get_uow().passports.get_by_school_id(school_id)

        self.assertEqual(passport.name, school.short_name)

    def test_existing_passport_not_changed(self):
        """Проверка игнорирования существующего паспорта при обновлении организации."""
        school_id = randint()

        initial_name = 'МБОУ СОШ 13'
        changed_name = 'МБОУ СОШ 14'

        bus.handle(schools.SchoolCreated(id=school_id, short_name=initial_name, status=True))
        passport = bus.get_uow().passports.get_by_school_id(school_id)

        self.assertEqual(passport.name, initial_name)

        bus.handle(schools.SchoolUpdated(id=school_id, short_name=changed_name))
        passport = bus.get_uow().passports.get_by_school_id(school_id)

        self.assertEqual(passport.name, initial_name)


class WorkModeTestCase(TransactionTestCase):
    def setUp(self):
        self.school = school_repo.add(schools.School(short_name='Школа №1', id=4815162342, status=True))
        passport_data = {
            'name': 'Библиотека имени В.В. Маяковского',
            'school_id': self.school.id,
        }
        self.passport = passport_repository.add(Passport(**passport_data))
        self.work_mode = {'schedule_mon_from': '08:00', 'lib_passport_id': self.passport.id}

    def test_create_work_mode(self) -> None:
        """Тест создания режима работы библиотеки."""
        command = CreateWorkMode(**self.work_mode)

        work_mode = bus.handle(command)

        self.assertIsNotNone(work_mode.id)
        db_work_mode = work_mode_repository.get_object_by_id(work_mode.id)
        for field, value in self.work_mode.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(work_mode, field), value)
                self.assertEqual(getattr(db_work_mode, field), value)
        self.assertEqual(db_work_mode.lib_passport_id, self.passport.id)

    def test_update_work_mode(self) -> None:
        """Тест обновления режима работы библиотеки."""
        work_mode = work_mode_repository.add(WorkMode(**self.work_mode))
        updated_fields = {
            'schedule_tue_from': '09:00',
        }
        command = UpdateWorkMode(id=work_mode.id, **updated_fields)

        result = bus.handle(command)

        db_work_mode = work_mode_repository.get_object_by_id(work_mode.id)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(result, field), value)
                self.assertEqual(getattr(db_work_mode, field), value)

    def test_delete_work_mode(self) -> None:
        """Тест удаления режима работы библиотеки."""
        work_mode = work_mode_repository.add(WorkMode(**self.work_mode))
        command = DeleteWorkMode(id=work_mode.id)

        bus.handle(command)

        with self.assertRaises(WorkModeNotFound):
            work_mode_repository.get_object_by_id(work_mode.id)

    def test_failed_commands(self) -> None:
        """Тест неудавшихся команд."""
        work_mode_repository.add(WorkMode(**self.work_mode))
        commands_with_errors = (
            (CreateWorkMode(**self.work_mode), 'lib_passport_id', 'Режим работы уже существует'),
            (CreateWorkMode(lib_passport_id=5000), 'lib_passport_id', 'Паспорт библиотеки не найден'),
            (UpdateWorkMode(id=10_000, ), 'id', 'Режим работы не найден'),
            (DeleteWorkMode(id=10_000), 'id', 'Режим работы не найден'),
        )

        for command, error, message in commands_with_errors:
            with self.subTest(command=command):
                with self.assertRaises(DomainValidationError) as exc:
                    bus.handle(command)

                self.assertIn(message, exc.exception.message_dict[error])
