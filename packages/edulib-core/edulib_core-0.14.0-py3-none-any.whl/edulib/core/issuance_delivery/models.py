import datetime

from django.db import (
    models,
)
from django.utils import (
    timezone,
)

from edulib.core.base.models import (
    BaseModel,
)
from edulib.core.lib_registry.models import (
    LibRegistryExample,
)
from edulib.core.readers.models import (
    Reader,
)

from . import (
    domain,
)


class IssuanceDelivery(BaseModel):
    """Выдача - сдача экземпляров."""

    MAX_LEASE_DATE = datetime.date(datetime.MAXYEAR, 1, 1)

    issuance_date = models.DateField(
        verbose_name=domain.IssuanceDelivery.issuance_date.title,
    )
    reader = models.ForeignKey(
        Reader,
        verbose_name=domain.IssuanceDelivery.reader_id.title,
        on_delete=models.CASCADE,
    )
    example = models.ForeignKey(
        LibRegistryExample,
        verbose_name=domain.IssuanceDelivery.example_id.title,
        on_delete=models.CASCADE,
    )
    fact_delivery_date = models.DateField(
        verbose_name=domain.IssuanceDelivery.fact_delivery_date.title,
        null=True,
        blank=True,
    )
    special_notes = models.CharField(
        verbose_name=domain.IssuanceDelivery.special_notes.title,
        max_length=domain.IssuanceDelivery.special_notes.max_length,
        null=True,
        blank=True,
    )
    extension_days_count = models.PositiveIntegerField(
        verbose_name=domain.IssuanceDelivery.extension_days_count.title,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'lib_iss_del'

    @property
    def expired(self) -> bool:
        """True если срок возврата экземпляра истек."""
        return self.delivery_date < timezone.now().date()

    @property
    def expired_date_str(self) -> str:
        """Дата возврата экземпляра."""
        if self.delivery_date == self.MAX_LEASE_DATE:
            return ''

        return self.delivery_date.strftime('%d.%m.%Y')

    def get_expired_message(self, wrap_expired: bool = False) -> str:
        if self.expired:
            msg = f'{self.expired_date_str} (просрочен)'
            if wrap_expired:
                msg = f'<span style="color:red">{msg}</span>'
            return msg

        return self.expired_date_str or 'неизвестно'

    # TODO rename `end_time_lease`
    @property
    def delivery_date(self) -> datetime.date:
        """Дата возврата экземпляра."""
        try:
            max_days = int(self.example.max_date) or 0
        except (TypeError, ValueError):
            return self.MAX_LEASE_DATE

        return self.issuance_date + datetime.timedelta(days=max_days)

    @property
    def approx_delivery_date(self) -> str:
        return self.get_expired_message()

    @property
    def approx_delivery_date_span(self) -> str:
        return self.get_expired_message(wrap_expired=True)

    @property
    def author_and_title(self) -> str:
        return f'{self.authors} / {self.title}'

    @property
    def title(self) -> str:
        return self.example.lib_reg_entry.title

    @property
    def authors(self) -> str:
        return self.example.lib_reg_entry.author.name

    @property
    def classbook_type(self) -> bool:
        return self.example.classbook_type
