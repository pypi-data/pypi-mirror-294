from datetime import (
    timedelta,
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
from edulib.core.issuance_delivery.domain import (
    AutoIssueExamples,
    DeliverExamples,
    IssueExamples,
    ProlongIssuance,
)
from edulib.core.issuance_delivery.tests.utils import (
    get_issuance_delivery,
)
from edulib.core.lib_registry.tests.utils import (
    get_registry_example,
)
from edulib.core.readers.tests.utils import (
    get_reader,
)
from edulib.core.schools.tests.utils import (
    get_school,
)


class IssuanceDeliveryTestCase(TransactionTestCase):
    def setUp(self) -> None:
        self.uow = bus.get_uow()

        self.school = get_school(self.uow)
        self.example = get_registry_example(self.uow, school_id=self.school.id)
        self.reader = get_reader(self.uow, school_id=self.school.id)

        self.initial_data = {
            'example_id': self.example.id,
            'reader_id': self.reader.id,
            'issuance_date': timezone.now().date() - timedelta(days=30),
        }

    def test_issue_example(self) -> None:
        command = IssueExamples(**self.initial_data, examples=[self.example.id])

        issuance_delivery, *_ = bus.handle(command)

        self.assertIsNotNone(issuance_delivery.id)
        db_issuance_delivery = self.uow.issuance_deliveries.get_object_by_id(issuance_delivery.id)
        for field, value in self.initial_data.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(issuance_delivery, field), value)
                self.assertEqual(getattr(db_issuance_delivery, field), value)

    def test_deliver_example(self) -> None:
        issuance_delivery = get_issuance_delivery(self.uow, **self.initial_data, school_id=self.school.id)
        delivery_data = {
            'fact_delivery_date': timezone.now().date(),
            'special_notes': 'Замечаний нет',
        }
        command = DeliverExamples(issued_ids=[issuance_delivery.id], **delivery_data)

        issuance_delivery, *_ = bus.handle(command)

        db_issuance_delivery = self.uow.issuance_deliveries.get_object_by_id(issuance_delivery.id)
        for field, value in delivery_data.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(issuance_delivery, field), value)
                self.assertEqual(getattr(db_issuance_delivery, field), value)

    def test_prolong_issuance(self) -> None:
        issuance_delivery = get_issuance_delivery(self.uow, **self.initial_data, school_id=self.school.id)
        prolong_data = {
            'extension_days_count': 10,
        }
        command = ProlongIssuance(id=issuance_delivery.id, **prolong_data)

        issuance_delivery = bus.handle(command)

        db_issuance_delivery = self.uow.issuance_deliveries.get_object_by_id(issuance_delivery.id)
        for field, value in prolong_data.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(issuance_delivery, field), value)
                self.assertEqual(getattr(db_issuance_delivery, field), value)

    def test_auto_issue_examples(self) -> None:
        command = AutoIssueExamples(
            issuance_date=self.initial_data['issuance_date'],
            count=1,
            issued=[
                {
                    'reader_id': self.initial_data['reader_id'],
                    'book_registry_ids': [self.example.lib_reg_entry_id],
                }
            ],
        )

        issuance_delivery, *_ = bus.handle(command)

        db_issuance_delivery = self.uow.issuance_deliveries.get_object_by_id(issuance_delivery.id)
        for field, value in self.initial_data.items():
            with self.subTest(field=field):
                self.assertEqual(getattr(issuance_delivery, field), value)
                self.assertEqual(getattr(db_issuance_delivery, field), value)

    def test_failed_commands(self) -> None:
        """Тест неудавшихся команд."""
        issuance_delivery = get_issuance_delivery(self.uow, **self.initial_data, school_id=self.school.id)
        commands_with_errors = (
            (
                IssueExamples(**self.initial_data, examples=[10_000]),
                'example_id',
                'Экземпляр библиотечного издания не найден',
            ),
            (
                IssueExamples(**self.initial_data | {'reader_id': 10_000, 'examples': [self.example.id]}),
                'reader_id',
                'Читатель не найден',
            ),
            (
                IssueExamples(**self.initial_data, examples=[self.example.id]),
                'example_id',
                'Экземпляр библиотечного издания уже выдан',
            ),
            (
                DeliverExamples(issued_ids=[10_000], fact_delivery_date=timezone.now()),
                'id',
                'Выдача экземпляра не найдена',
            ),
            (
                DeliverExamples(
                    issued_ids=[issuance_delivery.id],
                    fact_delivery_date=issuance_delivery.issuance_date - timedelta(days=1),
                ),
                'fact_delivery_date',
                'Фактическая дата сдачи экземпляра не может быть раньше даты выдачи экземпляра издания',
            ),
            (
                ProlongIssuance(id=10_000, extension_days_count=5),
                'id',
                'Выдача экземпляра не найдена',
            ),
            (
                AutoIssueExamples(
                    issuance_date=self.initial_data['issuance_date'],
                    count=2,
                    issued=[
                        {
                            'reader_id': self.initial_data['reader_id'],
                            'book_registry_ids': [self.example.lib_reg_entry_id],
                        }
                    ],
                ),
                '__root__',
                'Выбраны издания, у которых недостаточное для выдачи количество экземпляров',
            ),
        )

        for command, error, message in commands_with_errors:
            with self.subTest(message=message, command=command):
                with self.assertRaises(DomainValidationError) as exc:
                    bus.handle(command)
                self.assertIn(message, exc.exception.message_dict[error])
