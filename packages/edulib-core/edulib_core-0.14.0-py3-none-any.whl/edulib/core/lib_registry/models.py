"""Модели библиотечного реестра."""
# pylint: disable=too-many-lines, broad-exception-caught, import-outside-toplevel, consider-using-f-string
import datetime
import logging
from collections import (
    defaultdict,
)

from django.conf import (
    settings,
)
from django.db import (
    models,
)
from django.db.models import (
    CASCADE,
    Count,
    Q,
)
from django.db.transaction import (
    atomic,
)
from django.template.defaultfilters import (
    safe,
)
from sorl.thumbnail import (
    get_thumbnail,
)

import edulib
from edulib.core.base.files import (
    upload_file_handler,
    upload_named_handler,
)
from edulib.core.base.models import (
    BaseModel,
    SimpleDictionary,
)
from edulib.core.directory.models import (
    Catalog,
)
from edulib.core.lib_example_types.models import (
    LibraryExampleType,
)
from edulib.core.lib_registry import (
    domain,
)
from edulib.core.lib_registry.enums import (
    DefaultSectionsBBC,
    WriteoffReasonEnum,
)
from edulib.core.lib_sources.models import (
    LibrarySource,
)
from edulib.core.lib_udc.models import (
    LibraryUDC,
)


class LibMarkInformProduct(SimpleDictionary):
    """Справочник знаков информационной продукции"""

    def display(self):
        return self.code

    class Meta:
        db_table = 'lib_mark_prod'
        verbose_name = 'Знак информационной продукции'


class LibRegistryEntry(BaseModel):
    """Библиотечное издание."""

    type = models.ForeignKey(
        LibraryExampleType,
        verbose_name=domain.RegistryEntry.type_id.title,
        on_delete=models.CASCADE,
    )
    title = models.CharField(
        verbose_name=domain.RegistryEntry.title.title,
        max_length=domain.RegistryEntry.title.max_length,
    )
    author = models.ForeignKey(
        to='lib_authors.LibraryAuthors',
        verbose_name=domain.RegistryEntry.author_id.title,
        on_delete=models.CASCADE,
    )
    parallels = models.ManyToManyField(
        to='parallels.Parallel',
        through='RegistryEntryParallel',
        verbose_name=domain.RegistryEntry.parallel_ids.title,
        through_fields=('entry', 'parallel'),
    )
    author_sign = models.CharField(
        verbose_name=domain.RegistryEntry.author_sign.title,
        max_length=domain.RegistryEntry.author_sign.max_length,
        default=domain.RegistryEntry.author_sign.default,
        null=True,
        blank=True,
    )
    udc = models.ForeignKey(
        LibraryUDC,
        verbose_name=domain.RegistryEntry.udc_id.title,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    bbc = models.ForeignKey(
        Catalog,
        verbose_name=domain.RegistryEntry.bbc_id.title,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    discipline_id = models.BigIntegerField(
        verbose_name=domain.RegistryEntry.discipline_id.title,
        null=True,
        blank=True,
    )
    age_tag = models.ForeignKey(
        LibMarkInformProduct,
        verbose_name=domain.RegistryEntry.age_tag_id.title,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    tags = models.CharField(
        verbose_name=domain.RegistryEntry.tags.title,
        max_length=domain.RegistryEntry.tags.max_length,
        null=True,
        blank=True,
    )
    short_info = models.CharField(
        verbose_name=domain.RegistryEntry.short_info.title,
        max_length=domain.RegistryEntry.short_info.max_length,
        null=True,
        blank=True,
    )
    cover = models.ImageField(
        verbose_name=domain.RegistryEntry.cover.title,
        max_length=3 * 1024,
        upload_to=upload_file_handler,
        null=True,
        blank=True,
    )
    filename = models.FileField(
        verbose_name=domain.RegistryEntry.filename.title,
        max_length=255,
        upload_to=upload_named_handler,
        null=True,
        blank=True,
    )
    source = models.ForeignKey(
        LibrarySource,
        verbose_name=domain.RegistryEntry.source_id.title,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    on_balance = models.BooleanField(
        verbose_name=domain.RegistryEntry.on_balance.title,
        default=domain.RegistryEntry.on_balance.default,
    )
    school_id = models.BigIntegerField(
        verbose_name=domain.RegistryEntry.school_id.title,
    )
    take_from_fund = models.BooleanField(
        verbose_name=domain.RegistryEntry.take_from_fund.title,
        default=domain.RegistryEntry.take_from_fund.default,
    )
    all_in_fund = models.BooleanField(
        verbose_name=domain.RegistryEntry.all_in_fund.title,
        default=domain.RegistryEntry.all_in_fund.default,
    )
    status = models.PositiveSmallIntegerField(
        verbose_name=domain.RegistryEntry.status.title,
        choices=domain.EntryStatus.choices(),
        default=domain.EntryStatus.CURRENT,
    )
    federal_book = models.ForeignKey(
        to='federal_books.FederalBook',
        verbose_name=domain.RegistryEntry.federal_book_id.title,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def get_cover(self, size='', cover=None):
        r"""Возвращает url к обложке.

        Возвращает url к обложке, поппутно пытается его ресайзить
        size должен быть в формате ЧИСЛОxЧИСЛО
        (удовл. регулярке r'^(?P<x>\d+)?(?:x(?P<y>\d+))?$')
        """
        # Определяем наличие аватара
        cover = cover if cover else self.cover
        # всегда готовы вернуть аватар по умолчанию:
        result = self.get_cover_def()
        if result.startswith(settings.STATIC_ROOT):
            result = result.replace(settings.STATIC_ROOT, settings.STATIC_URL)
        # Если задан размер - попробуем преобразовать аватар:
        if cover and size:
            try:
                result = get_thumbnail(cover, size, quality=99)
            except Exception as err:
                logging.getLogger(__name__).exception(str(err))
        elif cover:
            # если задан автар без размера:
            result = cover
        result = result.url if hasattr(result, 'url') else result
        # TODO: нетерпимость к юникоду в урлах.
        # TODO: это может упасть при наличии кирилических именах папок
        assert isinstance(result, str), 'Error! Url must be a string!'
        if not result.startswith('/'):
            result = f'/{result}'
        # юникодные урлы неправильно распознаются. преобразуем к str
        result = str(result)
        result = result.replace('//', '/')
        return result

    def get_cover_def(self):
        return f'{settings.STATIC_ROOT}/library/img/no_cover.gif'

    @property
    def get_examples_count(self):

        # все экземпляры для данной карточки (не списанных)
        examples = LibRegistryExample.objects.filter(
            lib_reg_entry__id=self.id,
            writeoff_date__isnull=True
        )
        all_count = examples.count()

        from edulib.core.issuance_delivery.models import (
            IssuanceDelivery,
        )

        # количество экземпляров на руках у читателей
        at_users_count = IssuanceDelivery.objects.filter(
            Q(
                Q(fact_delivery_date__isnull=True) |
                Q(fact_delivery_date__gt=datetime.date.today())
            ),
            example__in=examples,
            issuance_date__isnull=False
        ).count()

        return '%d/%d' % (all_count, all_count - at_users_count)

    @atomic
    def save(self, *args, **kwargs):
        """Проверим запись в КСУ."""
        if self.id:
            presentEntry = LibRegistryEntry.objects.get(id=self.id)
            old_source = presentEntry.source
        else:
            old_source = self.source
        super().save(*args, **kwargs)
        if old_source != self.source:
            # Источник изменился, создадим записи в КСУ:
            for inflow_date in LibRegistryExample.objects.filter(
                lib_reg_entry=self
            ).values_list('inflow_date', flat=True):
                LibSummaryBook.objects.get_or_create(
                    school_id=self.school_id,
                    record_date=inflow_date,
                    source=self.source,
                )

    @property
    def classbook_type(self) -> bool:
        return self.type_id == LibraryExampleType.CLASSBOOK_ID

    class Meta:
        db_table = 'lib_registry'
        verbose_name = 'Библиотечное издание'
        verbose_name_plural = 'Библиотечные издания'


class RegistryEntryParallel(BaseModel):
    """Параллель библиотечного издания."""

    parallel = models.ForeignKey(
        'parallels.Parallel',
        verbose_name='Параллель',
        on_delete=models.CASCADE,
    )
    entry = models.ForeignKey(
        LibRegistryEntry,
        verbose_name='Библиотечное издание',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Параллель библиотечного издания'
        verbose_name_plural = 'Параллели библиотечных изданий'


class LibRegistryExample(BaseModel):
    """Экземпляр библиотечного издания."""

    lib_reg_entry = models.ForeignKey(
        LibRegistryEntry,
        verbose_name=domain.RegistryExample.lib_reg_entry_id.title,
        on_delete=models.CASCADE,
        related_name='examples',
    )
    invoice_number = models.CharField(
        verbose_name=domain.RegistryExample.invoice_number.title,
        max_length=domain.RegistryExample.invoice_number.max_length,
        blank=True,
    )
    card_number = models.CharField(
        verbose_name=domain.RegistryExample.card_number.title,
        max_length=domain.RegistryExample.card_number.max_length,
        null=True,
        blank=True,
    )
    inflow_date = models.DateField(
        verbose_name=domain.RegistryExample.inflow_date.title,
    )
    edition = models.CharField(
        verbose_name=domain.RegistryExample.edition.title,
        max_length=domain.RegistryExample.edition.max_length,
        null=True,
        blank=True,
    )
    edition_place = models.CharField(
        verbose_name=domain.RegistryExample.edition_place.title,
        max_length=domain.RegistryExample.edition_place.max_length,
    )
    edition_year = models.PositiveSmallIntegerField(
        verbose_name=domain.RegistryExample.edition_year.title,
    )
    publishing = models.ForeignKey(
        'lib_publishings.LibraryPublishings',
        verbose_name=domain.RegistryExample.publishing_id.title,
        on_delete=CASCADE,
        related_name='examples',
        null=True,
        blank=True,
    )
    # only digits
    duration = models.CharField(
        verbose_name=domain.RegistryExample.duration.title,
        max_length=domain.RegistryExample.duration.max_length,
    )
    book_code = models.CharField(
        verbose_name=domain.RegistryExample.book_code.title,
        max_length=domain.RegistryExample.book_code.max_length,
    )
    # only digits
    max_date = models.CharField(
        verbose_name=domain.RegistryExample.max_date.title,
        max_length=domain.RegistryExample.max_date.max_length,
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        verbose_name=domain.RegistryExample.price.title,
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
    )
    fin_source = models.SmallIntegerField(
        verbose_name=domain.RegistryExample.fin_source.title,
        choices=domain.FinSource.choices(),
        null=True,
        blank=True,
    )
    # вкладка СПИСАНИЕ
    writeoff_date = models.DateField(
        verbose_name='дата списания', null=True, blank=True)
    writeoff_reason = models.SmallIntegerField(
        choices=WriteoffReasonEnum.get_choices(), null=True, blank=True,
        verbose_name='причина списания')
    writeoff_act_number = models.CharField(
        max_length=50, verbose_name='номер акта выбытия', null=True)
    exchanged_example = models.ForeignKey(
        'self', null=True, blank=True, verbose_name='экземпляр заменен',
        on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Проверим запись в КСУ."""
        super().save(*args, **kwargs)

        # Проверим записи в КСУ:
        # - поступления:
        LibSummaryBook.objects.get_or_create(
            school_id=self.lib_reg_entry.school_id,
            record_date=self.inflow_date,
            source=self.lib_reg_entry.source,
        )
        # - выбытия:
        if self.writeoff_date:
            LibSummaryBookDisposal.objects.get_or_create(
                school_id=self.lib_reg_entry.school_id,
                record_date=self.writeoff_date,
                writeoff_act_number=self.writeoff_act_number,
            )
        # Снимем флаг законченного расчёта КСУ, чтобы пересчитать все значения
        calculated_lsb, _ = LibSummaryBookCalculated.objects.get_or_create(
            school_id=self.lib_reg_entry.school_id
        )
        if calculated_lsb.calculated:
            calculated_lsb.calculated = False
            calculated_lsb.note = ''
            calculated_lsb.save()

    def safe_delete(self):
        from edulib.core.issuance_delivery.models import (
            IssuanceDelivery,
        )

        # вместе с экземпляром удаляем и его историю выдачи
        IssuanceDelivery.objects.filter(example=self).delete()

        self.delete()
        return True

    @property
    def edition_info(self):
        """
        Получение выходных данных Место издания : Издательство : Год издания
        """
        return ': '.join([
            self.edition_place,
            '; '.join([
                self.publishing.name,
                str(self.edition_year)
            ])
        ])

    @property
    def busyness(self):
        """
        Получение занятости
        """
        from edulib.core.issuance_delivery.models import (
            IssuanceDelivery,
        )

        busyness_flag = IssuanceDelivery.objects.filter(
            Q(example=self, issuance_date__isnull=False),
            Q(fact_delivery_date__isnull=True) |
            Q(fact_delivery_date__gt=datetime.datetime.now().date())
        ).count()

        return 'Да' if busyness_flag else 'Нет'

    @property
    def get_type(self):
        return '%s' % self.lib_reg_entry.type.name

    @property
    def get_book_title(self) -> str:
        return self.lib_reg_entry.title

    @property
    def get_authors(self) -> str:
        return f'{self.lib_reg_entry.author}'

    @property
    def author_and_title(self) -> str:
        return ' / '.join((self.get_authors, self.get_book_title))

    @property
    def classbook_type(self) -> bool:
        return self.lib_reg_entry.classbook_type

    @property
    def inv_or_card_number(self):
        result = self.inv_number
        if self.classbook_type:
            result = self.card_number
        return result

    class Meta:
        db_table = 'lib_reg_examples'
        verbose_name = 'Экземпляр библиотечного издания'
        verbose_name_plural = 'Экземпляры библиотечных изданий'


class LibSummaryBook(BaseModel):
    """Книга суммарного учета."""

    audit_log = True

    school_id = models.BigIntegerField(
        verbose_name='Организация',
    )
    record_date = models.DateField(
        db_index=True,
        verbose_name='Дата записи в КСУ',
    )

    # Поступление:
    inflow_record_number = models.IntegerField(
        db_index=True,
        default=1,
        verbose_name='№ записи поступления'
    )
    source = models.ForeignKey(
        LibrarySource, blank=True, null=True, on_delete=models.CASCADE,
        verbose_name='Источник поступления',
    )
    document_date = models.DateField(
        blank=True, null=True,
        verbose_name='Дата сопров. документа',
    )
    document_number = models.CharField(
        blank=True, max_length=50, null=True,
        verbose_name='Номер сопров. документа',
    )
    examples_count = models.IntegerField(
        default=0,
        verbose_name='Поступило экземпляров'
    )
    names_count = models.IntegerField(
        default=0,
        verbose_name='Поступило названий'
    )
    examples_sum = models.DecimalField(
        decimal_places=2,
        default=0,
        max_digits=11,
        verbose_name='Поступило на сумму'
    )
    examples_on_balance_count = models.IntegerField(
        default=0,
        verbose_name='Поступило экземпляров, принятых на баланс'
    )
    names_on_balance_count = models.IntegerField(
        default=0,
        verbose_name='Поступило названий, принятых на баланс'
    )
    examples_on_balance_sum = models.DecimalField(
        decimal_places=2,
        default=0,
        max_digits=11,
        verbose_name='Поступило, принятых на баланс, на сумму'
    )
    examples_no_balance_count = models.IntegerField(
        default=0,
        verbose_name='Поступило экземпляров, не принятых на баланс'
    )
    names_no_balance_count = models.IntegerField(
        default=0,
        verbose_name='Поступило названий, не принятых на баланс'
    )
    examples_no_balance_sum = models.DecimalField(
        decimal_places=2,
        default=0,
        max_digits=11,
        verbose_name='Поступило, не принятых на баланс, на сумму'
    )

    @property
    def str_record_date(self):
        """Дата записи КСУ строкой (для сортировки в гриде)."""
        from .helpers import (
            get_date_for_grid,
        )
        return get_date_for_grid(self.record_date)

    @property
    def get_inflow_record_number(self):
        """Номер записи КСУ для вкладки "Поступление в фонд"."""
        libsummarybook_ids = LibSummaryBook.objects.filter(
            school=self.school,
            examples_count__gt=0,
        ).order_by(
            'record_date',
            'id',
            'source__name'
        ).values_list('id', flat=True)
        try:
            result = list(libsummarybook_ids).index(self.id) + 1
        except ValueError:
            result = libsummarybook_ids.count() + 1
        return result

    @property
    def inflow_document(self):
        """Дата и номер сопров. документа строкой."""
        from .helpers import (
            get_date_for_grid,
        )
        return safe('%s%s' % (
            get_date_for_grid(self.document_date),
            (' %s' % self.document_number) if self.document_number else ''
        )) if self.document_date or self.document_number else ''

    @property
    def get_examples(self):
        """Поступило экземпляров."""
        return LibRegistryExample.objects.filter(
            inflow_date=self.record_date,
            lib_reg_entry__source=self.source,
        ) if self.source else LibRegistryExample.objects.filter(
            inflow_date=self.record_date,
            lib_reg_entry__source__isnull=True,
        )

    @property
    def get_examples_count(self):
        """Кол-во поступивших экземпляров."""
        return self.get_examples.count()

    @property
    def get_names_count(self):
        """Кол-во поступивших названий."""
        return self.get_examples.values(
            'lib_reg_entry__book_title'
        ).distinct().count()

    @property
    def get_examples_sum(self):
        """Поступило экземпляров на сумму."""
        return self.get_examples.values('price').aggregate(
            total_price=models.Sum('price')
        )['total_price'] or 0

    @property
    def get_examples_on_balance(self):
        """Поступило экземпляров, принятых на баланс."""
        return self.get_examples.filter(
            lib_reg_entry__on_balance=True,
        )

    @property
    def get_examples_on_balance_count(self):
        """Кол-во поступивших экземпляров, принятых на баланс."""
        return self.get_examples_on_balance.count()

    @property
    def get_names_on_balance_count(self):
        """Кол-во поступивших названий, принятых на баланс."""
        return self.get_examples_on_balance.values(
            'lib_reg_entry__book_title'
        ).distinct().count()

    @property
    def get_examples_on_balance_sum(self):
        """Поступило экземпляров, принятых на баланс, на сумму."""
        return self.get_examples_on_balance.values('price').aggregate(
            total_price=models.Sum('price')
        )['total_price'] or 0

    @property
    def get_examples_no_balance_count(self):
        """Кол-во поступивших экземпляров, не принятых на баланс."""
        return (
            self.get_examples_count -
            self.get_examples_on_balance_count
        )

    @property
    def get_names_no_balance_count(self):
        """Кол-во поступивших названий, не принятых на баланс."""
        return (
            self.get_names_count -
            self.get_names_on_balance_count
        )

    @property
    def get_examples_no_balance_sum(self):
        """Поступило экземпляров, не принятых на баланс, на сумму."""
        return self.get_examples_sum - self.get_examples_on_balance_sum

    @property
    def get_examples_types_count(self):
        """Подсчет кол-ва поступивших экземпляров по типам."""
        result = defaultdict(int)
        for type_ in LibraryExampleType.objects.all():
            result[type_.id] = self.get_examples_on_balance.filter(
                lib_reg_entry__type=type_
            ).count()
        return result

    @property
    def examples_types_count(self):
        """Количество поступивших экземпляров по типам (по release_method)."""
        result = defaultdict(int)
        types_count = LibSummaryBookTypes.objects.filter(
            lib_summary_book=self,
        ).select_related('lib_example_type').values_list(
            'lib_example_type__release_method',
            'books_count',
        )
        for b_type, number in types_count:
            result[b_type] += number
        return result

    @property
    def get_examples_bbc_count(self):
        """Подсчет кол-ва поступивших экземпляров ББК."""
        result = defaultdict(int)
        for root_bbc in Catalog.objects.filter(parent__isnull=True):
            bbc_ids = root_bbc.get_descendants(
                include_self=True
            ).values_list('id', flat=True)
            result.update(dict.fromkeys(bbc_ids, 0))
            bbc_count_examples = self.get_examples_on_balance.filter(
                lib_reg_entry__bbc_id__in=bbc_ids
            ).values('lib_reg_entry__bbc_id').annotate(
                count=Count('id')
            ).values_list('lib_reg_entry__bbc_id', 'count')
            result.update(bbc_count_examples)

        return result

    @property
    def examples_bbc_count(self):
        """Количество поступивших экземпляров по корневым узлам ББК."""
        result = defaultdict(int)
        bbc_count_query = LibSummaryBookCatalog.objects.filter(
            lib_summary_book=self,
        )
        if edulib.get_config().use_default_bbc_sections:
            from edulib.core.lib_registry.helpers import (
                get_default_bbc_counts,
            )
            result = get_default_bbc_counts(bbc_count_query=bbc_count_query)

            # Производим расчет общего кол-ва поступивших учебников
            class_book_counts = LibSummaryBookTypes.objects.filter(
                lib_summary_book=self,
                lib_example_type=LibraryExampleType.CLASSBOOK_ID,
            ).annotate(
                sum_books_count=models.Sum('books_count')
            ).values_list('sum_books_count', flat=True)
            result[DefaultSectionsBBC.SCHOOLBOOK] = sum(class_book_counts)

        else:
            bbc_count = bbc_count_query.values_list(
                'bbc_id',
                'books_count',
            )
            result.update(bbc_count)

        return result

    class Meta():
        db_table = 'lib_summary_book'
        verbose_name = verbose_name_plural = 'Книга суммарного учета'


class LibSummaryBookTypes(BaseModel):
    """Количество документов по типам в книге суммарного учета."""

    lib_summary_book = models.ForeignKey(
        LibSummaryBook,
        on_delete=models.CASCADE,
        verbose_name='КСУ',
    )
    lib_example_type = models.ForeignKey(
        LibraryExampleType,
        on_delete=models.CASCADE,
        verbose_name='Тип библиотечного экземпляра',
    )
    books_count = models.IntegerField(
        default=0,
        verbose_name='Количество',
    )

    class Meta():

        db_table = 'lib_summary_book_types'
        verbose_name = 'Количество документов по типу в КСУ'
        verbose_name_plural = 'Количество документов по типам в КСУ'


class LibSummaryBookCatalog(BaseModel):
    """Количество документов по ББК в книге суммарного учета."""

    lib_summary_book = models.ForeignKey(
        LibSummaryBook,
        on_delete=models.CASCADE,
        verbose_name='КСУ',
    )
    bbc = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        verbose_name='раздел ББК',
    )
    books_count = models.IntegerField(
        default=0,
        verbose_name='Количество',
    )

    class Meta():

        db_table = 'lib_summary_book_catalog'
        verbose_name = verbose_name_plural = (
            'Количество документов по ББК в КСУ'
        )


class LibSummaryBookDisposal(BaseModel):
    """Книга суммарного учета - Выбытие."""

    audit_log = True

    school_id = models.BigIntegerField(
        verbose_name='Организация',
    )
    record_date = models.DateField(
        db_index=True,
        verbose_name='Дата записи в КСУ',
    )

    # Выбытие:
    writeoff_act_number = models.CharField(
        max_length=50,
        null=True,
        verbose_name='Номер акта выбытия',
    )
    disposal_source = models.TextField(
        null=True,
        verbose_name='Источники поступления'
    )
    examples_count = models.IntegerField(
        default=0,
        verbose_name='Выбыло экземпляров'
    )
    names_count = models.IntegerField(
        default=0,
        verbose_name='Выбыло названий'
    )
    examples_sum = models.DecimalField(
        decimal_places=2,
        default=0,
        max_digits=11,
        verbose_name='Выбыло на сумму'
    )
    examples_on_balance_count = models.IntegerField(
        default=0,
        verbose_name='Выбыло экземпляров, принятых на баланс'
    )
    names_on_balance_count = models.IntegerField(
        default=0,
        verbose_name='Выбыло названий, принятых на баланс'
    )
    examples_on_balance_sum = models.DecimalField(
        decimal_places=2,
        default=0,
        max_digits=11,
        verbose_name='Выбыло, принятых на баланс, на сумму'
    )
    examples_no_balance_count = models.IntegerField(
        default=0,
        verbose_name='Выбыло экземпляров, не принятых на баланс'
    )
    names_no_balance_count = models.IntegerField(
        default=0,
        verbose_name='Выбыло названий, не принятых на баланс'
    )
    examples_no_balance_sum = models.DecimalField(
        decimal_places=2,
        default=0,
        max_digits=11,
        verbose_name='Выбыло, не принятых на баланс, на сумму'
    )

    @atomic
    def save(self, *args, **kwargs):
        """Изменение № акта списания у экземпляров книг."""
        if self.id:
            presentDisposal = LibSummaryBookDisposal.objects.get(id=self.id)
            old_act_number = presentDisposal.writeoff_act_number
            examples = presentDisposal.get_examples
        else:
            old_act_number = self.writeoff_act_number
            examples = LibRegistryExample.objects.none()
        super().save(*args, **kwargs)
        if old_act_number != self.writeoff_act_number:
            examples.update(writeoff_act_number=self.writeoff_act_number)

    @property
    def str_record_date(self):
        """Дата записи КСУ строкой (для сортировки в гриде)."""
        from .helpers import (
            get_date_for_grid,
        )
        return get_date_for_grid(self.record_date)

    @property
    def get_disposal_source(self):
        """Источники поступлений выбывших экземпляров строкой."""
        return ', '.join(
            self.get_examples.filter(
                lib_reg_entry__source__isnull=False,
            ).order_by(
                'lib_reg_entry__source__name'
            ).values_list(
                'lib_reg_entry__source__name', flat=True
            ).distinct()
        )

    @property
    def get_examples(self):
        """Выбыло экземпляров."""
        examples = LibRegistryExample.objects.filter(
            writeoff_date=self.record_date,
            lib_reg_entry__school_id=self.school_id,
        )
        examples = examples.filter(
            writeoff_act_number=self.writeoff_act_number,
        ) if self.writeoff_act_number else examples.filter(
            writeoff_act_number__isnull=True,
        )
        return examples

    @property
    def get_examples_count(self):
        """Кол-во выбывших экземпляров."""
        return self.get_examples.count()

    @property
    def get_names_count(self):
        """Кол-во выбывших названий."""
        return self.get_examples.values(
            'lib_reg_entry__book_title'
        ).distinct().count()

    @property
    def get_examples_sum(self):
        """Выбыло экземпляров на сумму."""
        return self.get_examples.values('price').aggregate(
            total_price=models.Sum('price')
        )['total_price'] or 0

    @property
    def get_examples_on_balance(self):
        """Выбыло экземпляров, принятых на баланс."""
        return self.get_examples.filter(
            lib_reg_entry__on_balance=True,
        )

    @property
    def get_examples_on_balance_count(self):
        """Кол-во выбывших экземпляров, принятых на баланс."""
        return self.get_examples_on_balance.count()

    @property
    def get_names_on_balance_count(self):
        """Кол-во выбывших названий, принятых на баланс."""
        return self.get_examples_on_balance.values(
            'lib_reg_entry__book_title'
        ).distinct().count()

    @property
    def get_examples_on_balance_sum(self):
        """Выбыло экземпляров, принятых на баланс, на сумму."""
        return self.get_examples_on_balance.values(
            'price'
        ).aggregate(
            total_price=models.Sum('price')
        )['total_price'] or 0

    @property
    def get_examples_no_balance_count(self):
        """Кол-во выбывших экземпляров, не принятых на баланс."""
        return (
            self.get_examples_count -
            self.get_examples_on_balance_count
        )

    @property
    def get_names_no_balance_count(self):
        """Кол-во выбывших названий, не принятых на баланс."""
        return (
            self.get_names_count -
            self.get_names_on_balance_count
        )

    @property
    def get_examples_no_balance_sum(self):
        """Выбыло экземпляров, не принятых на баланс, на сумму."""
        return self.get_examples_sum - self.get_examples_on_balance_sum

    @property
    def get_examples_types_count(self):
        """Подсчет кол-ва выбывших экземпляров по типам."""
        result = defaultdict(int)
        for type_ in LibraryExampleType.objects.all():
            result[type_.id] = self.get_examples_on_balance.filter(
                lib_reg_entry__type=type_
            ).count()
        return result

    @property
    def examples_types_count(self):
        """Количество выбывших экземпляров по типам (по release_method).

        Используется модель LibSummaryBookDisposalTypes
        с заранее посчитанным количеством экземпляров по каждому типу.
        """
        result = defaultdict(int)
        types_count = LibSummaryBookDisposalTypes.objects.filter(
            lib_summary_book=self,
        ).select_related('lib_example_type').values_list(
            'lib_example_type__release_method',
            'books_count',
        )
        for b_type, number in types_count:
            result[b_type] += number
        return result

    @property
    def get_examples_bbc_count(self):
        """Подсчет кол-ва выбывших экземпляров ББК."""
        result = defaultdict(int)
        for root_bbc in Catalog.objects.filter(parent__isnull=True):
            bbc_ids = root_bbc.get_descendants(
                include_self=True
            ).values_list('id', flat=True)
            result.update(dict.fromkeys(bbc_ids, 0))
            bbc_count_examples = self.get_examples_on_balance.filter(
                lib_reg_entry__bbc_id__in=bbc_ids
            ).values('lib_reg_entry__bbc_id').annotate(
                count=Count('id')
            ).values_list('lib_reg_entry__bbc_id', 'count')
            result.update(bbc_count_examples)

        return result

    @property
    def examples_bbc_count(self):
        """Количество выбывших экземпляров по корневым узлам ББК.

        Используется модель LibSummaryBookDisposalCatalog
        с заранее посчитанным кол-вом экземпляров по каждому ББК.
        """
        result = defaultdict(int)
        bbc_count_query = LibSummaryBookDisposalCatalog.objects.filter(
            lib_summary_book=self,
        )
        if edulib.get_config().use_default_bbc_sections:
            from edulib.core.lib_registry.helpers import (
                get_default_bbc_counts,
            )
            result = get_default_bbc_counts(bbc_count_query=bbc_count_query)

            # Производим расчет общего кол-ва выбывших учебников
            class_book_counts = LibSummaryBookDisposalTypes.objects.filter(
                lib_summary_book=self,
                lib_example_type=LibraryExampleType.CLASSBOOK_ID,
            ).annotate(
                sum_books_count=models.Sum('books_count')
            ).values_list('sum_books_count', flat=True)
            result[DefaultSectionsBBC.SCHOOLBOOK] = sum(class_book_counts)

        else:
            for bbc in bbc_count_query:
                result[bbc.id] = bbc.books_count

        return result

    def get_examples_writeoff_reason_count(self) -> defaultdict:
        """Подсчёт количества выбывших экземпляров по причинам списания."""
        result = defaultdict(int)
        for reason in WriteoffReasonEnum.get_choices():
            result[reason[0]] = self.get_examples_on_balance.filter(
                writeoff_reason=reason[0],
            ).count()
        return result

    @property
    def examples_writeoff_reason_count(self):
        """Количество выбывших экземпляров по причинам списания.

        Используется модель с заранее посчитанным кол-вом экземпляров
        по каждой причине списания.
        """
        result = defaultdict(int)
        for reason in LibSummaryBookDisposalWriteoffReasons.objects.filter(
                lib_summary_book=self
        ):
            result[reason.writeoff_reason] = reason.books_count
        return result

    class Meta:

        db_table = 'lib_summary_book_disp'
        verbose_name = verbose_name_plural = (
            'Книга суммарного учета (выбытие)'
        )


class LibSummaryBookDisposalTypes(BaseModel):
    """Количество выбывших документов по типам в книге суммарного учета."""

    lib_summary_book = models.ForeignKey(
        LibSummaryBookDisposal,
        on_delete=models.CASCADE,
        verbose_name='КСУ',
    )
    lib_example_type = models.ForeignKey(
        LibraryExampleType,
        on_delete=models.CASCADE,
        verbose_name='Тип библиотечного экземпляра',
    )
    books_count = models.IntegerField(
        default=0,
        verbose_name='Количество',
    )

    class Meta():

        db_table = 'lib_summary_book_disp_types'
        verbose_name = 'Кол-во выбывших документов по типу в КСУ'
        verbose_name_plural = 'Кол-во выбывших документов по типам в КСУ'


class LibSummaryBookDisposalCatalog(BaseModel):
    """Количество выбывших документов по ББК в книге суммарного учета."""

    lib_summary_book = models.ForeignKey(
        LibSummaryBookDisposal,
        on_delete=models.CASCADE,
        verbose_name='КСУ',
    )
    bbc = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        verbose_name='раздел ББК',
    )
    books_count = models.IntegerField(
        default=0,
        verbose_name='Количество',
    )

    class Meta():

        db_table = 'lib_summary_book_disp_catalog'
        verbose_name = verbose_name_plural = (
            'Кол-во выбывших документов по ББК в КСУ'
        )


class LibSummaryBookDisposalWriteoffReasons(BaseModel):
    """Количество выбывших документов по причинам выбытия в КСУ."""

    lib_summary_book = models.ForeignKey(
        LibSummaryBookDisposal,
        on_delete=models.CASCADE,
        verbose_name='КСУ',
    )
    writeoff_reason = models.SmallIntegerField(
        choices=WriteoffReasonEnum.get_choices(),
        verbose_name='Причина списания')
    books_count = models.IntegerField(
        default=0,
        verbose_name='Количество',
    )

    class Meta:

        db_table = 'lib_summary_book_disp_writeoff_reasons'
        verbose_name = verbose_name_plural = (
            'Кол-во выбывших документов по причинам списания в КСУ')
        unique_together = ('lib_summary_book', 'writeoff_reason')


class LibExchangeFund(BaseModel):
    """Книгообменный фонд"""
    audit_log = True

    lib_reg_entry = models.ForeignKey(
        LibRegistryEntry,
        verbose_name='Карточка учета экземпляра',
        on_delete=CASCADE,
    )
    previous_lib_reg_entry_id = models.IntegerField(
        verbose_name='Инв. № копируемой карточки учета экземляра'
    )
    future_lib_reg_entry_id = models.IntegerField(
        verbose_name='Инв. № карточки учета экземляра '
                     'в случае передачи в школу-получатель',
        null=True, blank=True,
    )
    school_id = models.BigIntegerField(
        verbose_name='Школа'
    )
    teacher_id = models.BigIntegerField(
        verbose_name='Сотрудник'
    )
    phone = models.CharField(
        'Номер телефона', max_length=50, null=True, blank=True
    )
    date_from = models.DateField(
        verbose_name='Срок c', null=True, blank=True,
    )
    date_to = models.DateField(
        verbose_name='Срок по', null=True, blank=True,
    )
    note = models.CharField(
        max_length=256, null=True, blank=True,
        verbose_name='Примечание'
    )
    send_to_fund = models.BooleanField(
        default=False,
        verbose_name='Выдано из фонда в школу-получатель'
    )
    received_from_fund = models.BooleanField(
        default=True,
        verbose_name='Получено от школы-получателя обратно в фонд'
    )

    class Meta:
        db_table = 'lib_exchange_fund'


class LibSummaryBookCalculated(BaseModel):
    """Признак выполненных расчётов в книге суммарного учёта.

    После выполнения всех расчётов в КСУ по школе, значение поля calculated
    становится True. При добавлении или изменении экземпляра библиотеки
    значение поля calculated ставится False.
    """

    school_id = models.BigIntegerField(
        verbose_name='Школа',
    )
    calculated = models.BooleanField(
        default=False,
        verbose_name='Расчёт выполнен'
    )
    note = models.CharField(
        max_length=256, null=True, blank=True,
        verbose_name='Примечание'
    )

    class Meta:
        """Мета-настройки."""

        db_table = 'lib_summary_book_calculated'
        verbose_name = 'Вычисленная КСУ'
        verbose_name_plural = 'Вычисленные КСУ'
