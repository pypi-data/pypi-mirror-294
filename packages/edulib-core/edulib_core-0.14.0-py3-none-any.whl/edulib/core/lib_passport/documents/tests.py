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
from edulib.core.lib_passport.documents.adapters.db import (
    repository as document_repository,
)
from edulib.core.lib_passport.documents.domain import (
    CreateDocument,
    DeleteDocument,
    UpdateDocument,
)
from edulib.core.lib_passport.documents.domain.model import (
    Document,
    DocumentNotFound,
)
from edulib.core.lib_passport.domain import (
    Passport,
)
from edulib.core.schools.adapters.db import (
    repository as school_repo,
)
from edulib.core.schools.domain import (
    School,
)


class DocumentTestCase(TransactionTestCase):
    def setUp(self):
        self.initial_data = {
            'id': 4815162342,
            'short_name': 'СОШ №7',
            'status': True,
            'name': 'Средняя школа № 7',
        }
        self.initial_addresses = {
            'f_address': 'г. Казань, ул. Вымышленная, д. 1',
            'u_address': 'г. Казань, ул. Вымышленная, д. 2',
        }
        self.school = school_repo.add(School(**self.initial_data | self.initial_addresses))
        passport_data = {
            'name': 'Библиотека имени В.В. Маяковского',
            'school_id': self.school.id,
        }
        self.passport = passport_repository.add(Passport(**passport_data))
        self.document_data = {'name': 'Очень важный документ', 'doc_type': 1, 'library_passport_id': self.passport.id}

    def test_create_document(self) -> None:
        """Тест создания документа."""
        command = CreateDocument(**self.document_data)

        document = bus.handle(command)

        self.assertIsNotNone(document.id)
        db_document = document_repository.get_object_by_id(document.id)
        for field, value in self.document_data.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(document, field), value)
                self.assertEqual(getattr(db_document, field), value)
        self.assertEqual(db_document.library_passport_id, self.passport.id)

    def test_update_document(self) -> None:
        """Тест обновления документа."""
        document = document_repository.add(Document(**self.document_data))
        updated_fields = {
            'name': 'Крайне важный документ',
        }
        command = UpdateDocument(id=document.id, **updated_fields)

        result = bus.handle(command)

        db_document = document_repository.get_object_by_id(document.id)
        for field, value in updated_fields.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(result, field), value)
                self.assertEqual(getattr(db_document, field), value)

    def test_delete_document(self) -> None:
        """Тест удаления документа."""
        document = document_repository.add(Document(**self.document_data))
        command = DeleteDocument(id=document.id)

        bus.handle(command)

        with self.assertRaises(DocumentNotFound):
            document_repository.get_object_by_id(document.id)

    def test_failed_commands(self) -> None:
        """Тест неудавшихся команд."""
        document_repository.add(Document(**self.document_data))
        commands_with_errors = (
            (CreateDocument(**self.document_data), 'name', 'Документ уже существует'),
            (CreateDocument(library_passport_id=5000), 'library_passport_id', 'Паспорт библиотеки не найден'),
            (UpdateDocument(id=10_000, ), 'id', 'Документ не найден'),
            (DeleteDocument(id=10_000), 'id', 'Документ не найден'),
        )

        for command, error, message in commands_with_errors:
            with self.subTest(command=command):
                with self.assertRaises(DomainValidationError) as exc:
                    bus.handle(command)

                self.assertIn(message, exc.exception.message_dict[error])
