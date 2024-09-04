import datetime

from django.core.exceptions import (
    ValidationError,
)
from django.db import (
    models,
)
from django.db.models import (
    CASCADE,
)
from django.db.models.query import (
    Q,
)
from django.utils import (
    timezone,
)

from edulib.core.base.domain import (
    BaseEnumerate,
)
from edulib.core.base.models import (
    BaseModel,
)
from edulib.core.directory.models import (
    Catalog,
)
from edulib.core.lib_udc.models import (
    LibraryUDC,
)
from edulib.core.readers import (
    domain,
)

from .enums import (
    RequestStatusEnum,
)


class RoleTypeEnumerate(BaseEnumerate):

    STUDENT, TEACHER = 1, 2

    values = {
        STUDENT: 'Ученик',
        TEACHER: 'Сотрудник',
    }


class TrueFalseEnumerate(BaseEnumerate):

    YES, NO = 1, 0

    values = {
        YES: 'Да',
        NO: 'Нет',
    }


class SearchRequestType(BaseEnumerate):

    SIMPLE, ADVANCE = 0, 1

    values = {
        SIMPLE: 'Простой поиск',
        ADVANCE: 'Расширенный поиск',
    }


def current_year() -> int:
    """Возвращает текущий год."""
    return timezone.now().year


class Reader(BaseModel):
    """Читатель."""

    number = models.CharField(
        verbose_name=domain.Reader.number.title,
        max_length=domain.Reader.number.max_length,
        null=True,
    )
    schoolchild_id = models.BigIntegerField(
        verbose_name=domain.Reader.schoolchild_id.title,
        unique=True,
        null=True,
        blank=True,
    )
    teacher_id = models.BigIntegerField(
        verbose_name=domain.Reader.teacher_id.title,
        null=True,
        blank=True,
    )
    school_id = models.BigIntegerField(
        verbose_name=domain.Reader.school_id.title,
        null=True,
        blank=True,
    )
    year = models.CharField(
        verbose_name=domain.Reader.year.title,
        max_length=domain.Reader.year.max_length,
        default=current_year,
    )
    role = models.SmallIntegerField(
        verbose_name=domain.Reader.role.title,
        choices=domain.ReaderRole.choices(),
        default=domain.ReaderRole.STUDENT,
    )

    def save(self, *args, **kwargs):
        if Reader.objects.filter(
            number=self.number,
            school_id=self.school_id
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                'Указанный номер читательского билета уже используется!'
            )
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'library_readers'
        verbose_name = 'Читатель'
        verbose_name_plural = 'Читатели'
        unique_together = ('number', 'school_id')

    def safe_delete(self, *args, **kwargs):
        if self.debt.exists():
            raise ValidationError(
                'Невозможно удалить читателя, который<br/>'
                'имеет задолжности по книгам!')

        from ..issuance_delivery.models import IssuanceDelivery  # pylint: disable=import-outside-toplevel
        return self.delete_related(affected=[IssuanceDelivery])

    @property
    def debt(self):
        """Задолженности по библиотечным экземплярам"""
        return self.issuancedelivery_set.filter(
            Q(fact_delivery_date__isnull=True) |
            Q(fact_delivery_date__gt=datetime.date.today())
        )

    @property
    def debt_count(self):
        """Общее число задолженностей по библиотечным экземплярам"""
        return self.debt.count() or ''


class Reader2Response(BaseModel):
    responce_id = models.IntegerField(verbose_name='Отзыв')
    reader = models.ForeignKey(
        Reader, verbose_name='Читатель',
        on_delete=models.CASCADE)

    class Meta:
        db_table = 'library_reader_responce'


class SearchRequestHistory(BaseModel):

    """История запросов книг читателями. """

    REQUEST_SENT = 1
    REQUEST_PROCESSED = 2

    STATUSES_INFO = {
        REQUEST_SENT: 'Заявка отправлена',
        REQUEST_PROCESSED: 'Заявка обработана'
    }

    type = models.SmallIntegerField(
        choices=SearchRequestType.get_choices(),
        verbose_name='тип запроса'
    )
    reader = models.ForeignKey(
        Reader, verbose_name='читатель',
        on_delete=models.CASCADE)
    date = models.DateField(verbose_name='дата выполнения запроса')
    simple_request = models.CharField(
        max_length=300,
        verbose_name='текст запроса простого поиска',
        null=True, blank=True
    )
    book_title = models.CharField(
        max_length=350,
        verbose_name='заглавие',
        null=True, blank=True
    )
    authors = models.CharField(
        max_length=350,
        verbose_name='авторы',
        default='-',
        null=True, blank=True
    )
    udc = models.ForeignKey(
        LibraryUDC,
        verbose_name='раздел УДК',
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    bbc = models.ForeignKey(
        Catalog,
        verbose_name='раздел ББК',
        null=True,
        blank=True,
        on_delete=CASCADE,
    )
    discipline_id = models.IntegerField(
        verbose_name='предмет ФГОС', null=True, blank=True)
    tags = models.CharField(
        max_length=350,
        verbose_name='ключевые слова',
        null=True, blank=True
    )
    status = models.PositiveSmallIntegerField(
        choices=RequestStatusEnum.get_choices(),
        default=RequestStatusEnum.REQUEST_SENT, verbose_name='Статус'
    )
    parent_id = models.BigIntegerField(  # RENAME
        verbose_name='Родитель',
        null=True, blank=True,
    )

    class Meta:
        db_table = 'lib_reader_search_history'


class TeacherReview(BaseModel):

    reader = models.ForeignKey(
        Reader, verbose_name='читатель',
        on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)

    @property
    def created_prop(self):
        return self.created.date()

    class Meta:
        db_table = 'lib_teacher_review'
