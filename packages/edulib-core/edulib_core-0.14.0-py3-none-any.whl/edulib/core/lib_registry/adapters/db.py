import re
from collections.abc import (
    Generator,
)
from typing import (
    TYPE_CHECKING,
    Optional,
)

from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.db.models import (
    Count,
    DateField,
    Max,
    Q,
)
from django.db.models.expressions import (
    Exists,
    Func,
    OuterRef,
    Value,
)
from django.db.models.functions import (
    Coalesce,
)
from django.db.models.functions.text import (
    Upper,
)
from django.forms import (
    model_to_dict,
)
from django.utils import (
    timezone,
)
from explicit.adapters.db import (
    AbstractRepository,
)
from explicit.domain import (
    asdict,
)

from edulib.core.adapters.db import (
    AbstractRepository as LibAbstractRepository,
)
from edulib.core.lib_registry import (
    domain,
    models as db,
)


if TYPE_CHECKING:
    from edulib.core.federal_books.domain.model import (
        FederalBook,
    )


class ExchangeFundRepository(LibAbstractRepository):
    model = db.LibExchangeFund


exchange_fund = ExchangeFundRepository()


class InfoProductMarkRepository(AbstractRepository):
    def get_object_by_id(self, identifier: int) -> domain.InfoProductMark:
        try:
            db_instance = db.LibMarkInformProduct.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as exc:
            raise domain.InfoProductMarkNotFound from exc

    def add(self, obj: domain.InfoProductMark) -> domain.InfoProductMark:
        assert isinstance(obj, domain.InfoProductMark)

        return self._to_db(obj)

    def update(self, obj: domain.InfoProductMark) -> domain.InfoProductMark:
        assert isinstance(obj, domain.InfoProductMark)

        return self._to_db(obj)

    def delete(self, obj: domain.InfoProductMark) -> None:
        assert isinstance(obj, domain.InfoProductMark)

        db.LibMarkInformProduct.objects.filter(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[domain.InfoProductMark, None, None]:
        for entry in db.LibMarkInformProduct.objects.iterator():
            yield self._to_domain(entry)

    def _to_domain(self, db_instance: db.LibMarkInformProduct) -> domain.InfoProductMark:
        return domain.InfoProductMark(**model_to_dict(db_instance))

    def _to_db(self, modelinstance: domain.InfoProductMark) -> domain.InfoProductMark:
        assert isinstance(modelinstance, domain.InfoProductMark)

        db_instance, _ = self._base_qs.update_or_create(pk=modelinstance.id, defaults=asdict(modelinstance))
        modelinstance.id = db_instance.pk
        assert modelinstance.id is not None

        return modelinstance


info_product_marks = InfoProductMarkRepository()


class RegistryEntryRepository(AbstractRepository):
    def get_object_by_id(self, identifier: int) -> domain.RegistryEntry:
        try:
            db_instance = db.LibRegistryEntry.objects.prefetch_related('parallels').get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as exc:
            raise domain.RegistryEntryNotFound from exc

    def add(self, obj: domain.RegistryEntry) -> domain.RegistryEntry:
        assert isinstance(obj, domain.RegistryEntry)

        return self._to_db(obj)

    def update(self, obj: domain.RegistryEntry) -> domain.RegistryEntry:
        assert isinstance(obj, domain.RegistryEntry)

        return self._to_db(obj)

    def delete(self, obj: domain.RegistryEntry) -> None:
        assert isinstance(obj, domain.RegistryEntry)

        db.LibRegistryEntry.objects.filter(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[domain.RegistryEntry, None, None]:
        for entry in db.LibRegistryEntry.objects.iterator():
            yield self._to_domain(entry)

    def _to_db(self, modelinstance: domain.RegistryEntry) -> domain.RegistryEntry:
        assert isinstance(modelinstance, domain.RegistryEntry)

        if cover := modelinstance.cover:
            modelinstance.cover = None  # ошибка при вызове asdict

        db_instance, _ = db.LibRegistryEntry.objects.update_or_create(
            pk=modelinstance.id,
            defaults=asdict(modelinstance, exclude=['parallel_ids']) | {'cover': cover},
        )
        if modelinstance.parallel_ids:
            db_instance.parallels.set(parallel for parallel in modelinstance.parallel_ids)

        return self.get_object_by_id(db_instance.pk)

    def _to_domain(self, dbinstance: db.LibRegistryEntry) -> domain.RegistryEntry:
        registry_entry = domain.RegistryEntry(
            type_id=dbinstance.type_id,
            author_id=dbinstance.author_id,
            bbc_id=dbinstance.bbc_id,
            udc_id=dbinstance.udc_id,
            source_id=dbinstance.source_id,
            age_tag_id=dbinstance.age_tag_id,
            federal_book_id=dbinstance.federal_book_id,
            **model_to_dict(dbinstance, exclude=['author', 'type', 'bbc', 'udc', 'source', 'age_tag', 'federal_book']),
        )
        registry_entry.parallel_ids = [parallel.id for parallel in dbinstance.parallels.all()]

        return registry_entry

    def has_similar(self, entry: domain.RegistryEntry, federal_book: Optional['FederalBook']) -> bool:
        """Проверяет уникальность элемента библиотечного реестра."""
        query = db.LibRegistryEntry.objects.exclude(id=entry.id).filter(type=entry.type_id, school_id=entry.school_id)

        if federal_book:
            query = query.annotate(
                comparable_title=Value(federal_book.name.upper().replace(' ', '')),
            ).filter(
                comparable_title=strip_str(federal_book.name).upper(),
                author=federal_book.authors,
            )
        else:
            query = query.annotate(
                comparable_title=Func(Upper('title'), Value(' '), Value(''), function='replace'),
            ).filter(
                comparable_title=strip_str(entry.title).upper(),
                author=entry.author_id,
            )

        return query.exists()

    def has_examples(self, entry: domain.RegistryEntry) -> bool:
        return db.LibRegistryExample.objects.filter(lib_reg_entry_id=entry.id).exists()

    def get_school_entries_not_in_fund(self, school_id):
        """Карточки учета экземпляров книг, принадлежащих школе и которые не находятся в книгообменном фонде."""
        exchange_fund_subquery = db.LibExchangeFund.objects.filter(
            lib_reg_entry_id=OuterRef('pk'),
        )

        entries = (
            db.LibRegistryEntry.objects.filter(school_id=school_id)
            .annotate(exchange_exists=Exists(exchange_fund_subquery))
            .filter(exchange_exists=False)
        )

        return entries


registry_entries = RegistryEntryRepository()


class RegistryExampleRepository(AbstractRepository):
    def get_object_by_id(self, identifier: int) -> domain.RegistryExample:
        try:
            db_instance = db.LibRegistryExample.objects.get(pk=identifier)
            return self._to_domain(db_instance)
        except ObjectDoesNotExist as exc:
            raise domain.RegistryExampleNotFound from exc

    def add(self, obj: domain.RegistryExample) -> domain.RegistryExample:
        assert isinstance(obj, domain.RegistryExample)

        return self._to_db(obj)

    def update(self, obj: domain.RegistryExample) -> domain.RegistryExample:
        assert isinstance(obj, domain.RegistryExample)

        return self._to_db(obj)

    def delete(self, obj: domain.RegistryExample) -> None:
        assert isinstance(obj, domain.RegistryExample)

        db.LibRegistryExample.objects.filter(pk=obj.id).delete()

    def get_all_objects(self) -> Generator[domain.RegistryExample, None, None]:
        for entry in db.LibRegistryExample.objects.iterator():
            yield self._to_domain(entry)

    def get_available_examples(
        self,
        lib_reg_entry_id: int,
        count: Optional[int] = None,
    ) -> list[domain.RegistryExample]:
        now = timezone.now()
        examples = db.LibRegistryExample.objects.annotate(
            max_delivery_date=Max(
                Coalesce(
                    'issuancedelivery__fact_delivery_date',
                    Value('9999-12-31'),
                    output_field=DateField(),
                )
            ),
            issuancedelivery_count=Count('issuancedelivery'),
        ).filter(
            Q(issuancedelivery_count=0) | Q(max_delivery_date__lt=now),
            Q(writeoff_date__isnull=True) | Q(writeoff_date__gt=now),
            lib_reg_entry_id=lib_reg_entry_id,
        )
        if count:
            examples = examples[:count]

        return [self._to_domain(example) for example in examples]

    def examples_count(self, example: domain.RegistryExample) -> int:
        return db.LibRegistryExample.objects.filter(
            lib_reg_entry_id=example.lib_reg_entry_id,
        ).count()

    def _to_db(self, modelinstance: domain.RegistryExample) -> domain.RegistryExample:
        assert isinstance(modelinstance, domain.RegistryExample)

        if modelinstance.id is None:
            db_instance = db.LibRegistryExample()
        else:
            db_instance = db.LibRegistryExample.objects.filter(pk=modelinstance.id).first() or db.LibRegistryExample()

        for field in modelinstance.__dataclass_fields__:
            if field == 'id':
                continue
            setattr(db_instance, field, getattr(modelinstance, field))

        db_instance.save(exclude_not_null_fields=['invoice_number'])
        modelinstance.id = db_instance.pk

        return modelinstance

    def _to_domain(self, dbinstance: db.LibRegistryEntry) -> domain.RegistryExample:
        return domain.RegistryExample(
            lib_reg_entry_id=dbinstance.lib_reg_entry_id,
            publishing_id=dbinstance.publishing_id,
            **model_to_dict(dbinstance, exclude=['lib_reg_entry', 'publishing']),
        )


registry_examples = RegistryExampleRepository()


def strip_str(text: str) -> str:
    """Убирает из строки пробелы и кавычки. Нужна для сравнения."""
    return re.sub('["\' ]', '', text) if text else ''
