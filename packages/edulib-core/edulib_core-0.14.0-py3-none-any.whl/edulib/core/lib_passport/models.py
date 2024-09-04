"""Паспорт библиотеки. Модели."""
from django.db import (
    models,
)

from edulib.core import (
    domain,
)
from edulib.core.base.models import (
    BaseModel,
)


class LibPassport(BaseModel):
    """Паспорт библиотеки."""

    school = models.OneToOneField(
        db_constraint=False,
        verbose_name='Идентификатор ОО',
        to='schools.School',
        on_delete=models.DO_NOTHING,
    )
    name = models.CharField(
        max_length=250,
        verbose_name='Наименование библиотеки',
    )
    date_found_month = models.SmallIntegerField(
        verbose_name='Дата основания (месяц)',
        choices=domain.MonthEnum.get_choices(),
        null=True,
        blank=True,
    )
    date_found_year = models.PositiveSmallIntegerField(
        verbose_name='Дата основания (год)',
        null=True,
        blank=True,
    )
    library_chief = models.ForeignKey(
        verbose_name='Заведующий библиотекой',
        to='employees.Employee',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True
    )
    is_address_match = models.BooleanField(
        verbose_name='Адрес совпадает с адресом ОО',
        default=False,
    )
    is_telephone_match = models.BooleanField(
        verbose_name='Телефон совпадает с телефоном ОО',
        default=False,
    )
    telephone = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    is_email_match = models.BooleanField(
        verbose_name='Email совпадает с email ОО',
        default=False,
    )
    email = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    academic_year = models.ForeignKey(
        verbose_name='Период обучения',
        to='academic_years.AcademicYear',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
    )
    address = models.ForeignKey(
        verbose_name='Идентификатор адреса',
        to='address.Address',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'library_passport'
        verbose_name = 'Паспорт библиотеки'
        verbose_name_plural = 'Паспорт библиотеки'

    def __str__(self):
        """Строковое представление объекта."""
        # pylint: disable=invalid-str-returned
        return self.name


class WorkMode(BaseModel):
    """Режим работы библиотеки."""

    lib_passport = models.OneToOneField(
        verbose_name='Паспорт библиотеки',
        to='lib_passport.LibPassport',
        on_delete=models.CASCADE,
        related_name='work_mode',
    )
    schedule_mon_from = models.CharField(
        max_length=10,
        verbose_name='Режим работы с - Понедельник',
        null=True,
        blank=True,
    )
    schedule_mon_to = models.CharField(
        max_length=10,
        verbose_name='Режим работы по - Понедельник',
        null=True,
        blank=True,
    )
    schedule_tue_from = models.CharField(
        max_length=10,
        verbose_name='Режим работы с - Вторник',
        null=True,
        blank=True,
    )
    schedule_tue_to = models.CharField(
        max_length=10,
        verbose_name='Режим работы по - Вторник',
        null=True,
        blank=True,
    )
    schedule_wed_from = models.CharField(
        max_length=10,
        verbose_name='Режим работы с - Среда',
        null=True,
        blank=True,
    )
    schedule_wed_to = models.CharField(
        max_length=10,
        verbose_name='Режим работы по - Среда',
        null=True,
        blank=True,
    )
    schedule_thu_from = models.CharField(
        max_length=10,
        verbose_name='Режим работы с - Четверг',
        null=True,
        blank=True,
    )
    schedule_thu_to = models.CharField(
        max_length=10,
        verbose_name='Режим работы по - Четверг',
        null=True,
        blank=True,
    )
    schedule_fri_from = models.CharField(
        max_length=10,
        verbose_name='Режим работы с - Пятница',
        null=True,
        blank=True,
    )
    schedule_fri_to = models.CharField(
        max_length=10,
        verbose_name='Режим работы по - Пятница',
        null=True,
        blank=True,
    )
    schedule_sat_from = models.CharField(
        max_length=10,
        verbose_name='Режим работы с - Суббота',
        null=True,
        blank=True,
    )
    schedule_sat_to = models.CharField(
        max_length=10,
        verbose_name='Режим работы по- Суббота',
        null=True,
        blank=True,
    )
    schedule_sun_from = models.CharField(
        max_length=10,
        verbose_name='Режим работы с - Воскресенье',
        null=True,
        blank=True,
    )
    schedule_sun_to = models.CharField(
        max_length=10,
        verbose_name='Режим работы по - Воскресенье',
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'library_work_mode'
        verbose_name = 'Режим работы библиотеки'
        verbose_name_plural = 'Режим работы библиотеки'
