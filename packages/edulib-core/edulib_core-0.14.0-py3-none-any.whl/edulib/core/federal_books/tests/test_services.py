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
from edulib.core.federal_books.adapters.db import (
    repository,
)
from edulib.core.federal_books.domain import (
    CreateFederalBook,
    FederalBook,
    UpdateFederalBook,
)
from edulib.core.lib_authors.adapters.db import (
    repository as authors_rep,
)
from edulib.core.lib_authors.domain.model import (
    Author,
)
from edulib.core.lib_publishings.adapters.db import (
    repository as pub_rep,
)
from edulib.core.lib_publishings.domain.model import (
    Publishing,
)
from edulib.core.parallels.adapters.db import (
    repository as parallel_rep,
)
from edulib.core.parallels.domain import (
    Parallel,
)


class FederalBookTestCase(TransactionTestCase):

    def setUp(self) -> None:
        """Подготавливает данные для тестов."""
        self.publishing = pub_rep.add(Publishing(name='Питер'))
        self.author = authors_rep.add(Author(name='Бунимович Е.А., Кузнецова Л.В., Минаева С.С. и другие'))
        self.parallel = parallel_rep.add(Parallel(id=315827, system_object_id=0, title=1, object_status=True))

        self.federal_book = {
            'name': 'Алгебра',
            'authors': self.author.id,
            'parallel_ids': [self.parallel.id, ],
            'code': '1.1.2.4.2.2.1.',
            'validity_period': date(2027, 8, 31),
            'publishing_id': self.publishing.id
        }

        self.for_modified_params = self.federal_book.copy()
        self.for_modified_params['name'] = ''

    def test_create_federal_book(self) -> None:
        """Тест создания учебника федерального перечня учебников."""
        command = CreateFederalBook(**self.federal_book)

        federal_book = bus.handle(command)

        self.assertIsNotNone(federal_book.id)
        db_federal_book = repository.get_object_by_id(federal_book.id)
        for field, value in self.federal_book.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(federal_book, field), value)
                self.assertEqual(getattr(db_federal_book, field), value)

    def test_update_federal_book(self) -> None:
        """Тест обновления учебника федерального перечня учебников."""
        federal_book = repository.add(FederalBook(**self.federal_book))
        updated_fields = {
            'status': False,
        }
        command = UpdateFederalBook(id=federal_book.id, **updated_fields)

        result = bus.handle(command)

        db_federal_book = repository.get_object_by_id(federal_book.id)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(result, field), value)
                self.assertEqual(getattr(db_federal_book, field), value)

    def test_failed_commands(self) -> None:
        """Тест неудавшихся команд."""
        repository.add(FederalBook(**self.federal_book))
        commands_with_errors = ((
                                    CreateFederalBook(**self.federal_book),
                'name',
                'Такой учебник уже существует в Федеральном перечне учебников'
            ),
            (CreateFederalBook(**self.for_modified_params), 'name', 'Наименование не может быть пустым'),
        )

        for command, error, message in commands_with_errors:
            with self.subTest(command=command):
                with self.assertRaises(DomainValidationError) as exc:
                    bus.handle(command)

                self.assertIn(message, exc.exception.message_dict[error])
