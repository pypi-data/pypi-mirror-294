from datetime import (
    date,
)

from django.test import (
    TransactionTestCase,
)
from explicit.domain.validation.exceptions import (
    DomainValidationError,
)

from edulib.core import (
    bus,
)
from edulib.core.lib_passport.adapters.db import (
    passport_repository,
)
from edulib.core.lib_passport.cleanup_days.adapters.db import (
    repository as cleanup_days_repo,
)
from edulib.core.lib_passport.cleanup_days.domain import (
    CleanupDay,
    CleanupDayNotFound,
    CreateCleanupDay,
    DeleteCleanupDay,
)
from edulib.core.lib_passport.domain.model import (
    Passport,
)
from edulib.core.schools.adapters.db import (
    repository as school_repo,
)
from edulib.core.schools.domain import (
    School,
)


class CleanupDayTestCase(TransactionTestCase):

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.school = school_repo.add(School(short_name='Школа №1', id=4815162342, status=True))
        self.passport_data = {
            'name': 'Библиотека имени В.В. Маяковского',
            'school_id': self.school.id,
        }
        self.passport = passport_repository.add(Passport(**self.passport_data))
        self.cleanup_day_data = {
            'cleanup_date': date(2024, 6, 18),
            'lib_passport_id': self.passport.id
        }

    def test_create_cleanup_day(self) -> None:
        """Тест создания санитарного дня."""
        command = CreateCleanupDay(**self.cleanup_day_data)

        cleanup_day = bus.handle(command)

        self.assertIsNotNone(cleanup_day.id)
        db_cleanup_day = cleanup_days_repo.get_object_by_id(cleanup_day.id)

        self.assertEqual(db_cleanup_day.cleanup_date, self.cleanup_day_data['cleanup_date'])

    def test_delete_cleanup_day(self) -> None:
        """Тест удаления санитарного дня."""
        cleanup_day = cleanup_days_repo.add(CleanupDay(**self.cleanup_day_data))

        command = DeleteCleanupDay(id=cleanup_day.id, lib_passport_id=cleanup_day.lib_passport_id)

        bus.handle(command)

        with self.assertRaises(CleanupDayNotFound):
            cleanup_days_repo.get_object_by_id(cleanup_day.id)

    def test_failed_commands(self) -> None:
        """Тест неудавшихся команд."""
        cleanup_days_repo.add(CleanupDay(**self.cleanup_day_data))
        commands_with_errors = (
            (CreateCleanupDay(**self.cleanup_day_data), 'cleanup_date', 'Санитарный день уже существует'),
            (DeleteCleanupDay(lib_passport_id=self.passport.id, id=10_000), 'id', 'Санитарный день не найден'),
        )

        for command, error, message in commands_with_errors:
            with self.subTest(command=command):
                with self.assertRaises(DomainValidationError) as exc:
                    bus.handle(command)

                self.assertIn(message, exc.exception.message_dict[error])
