from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)

from . import (
    domain,
)


class Parent(BaseModel):
    """Проекция "Представитель"."""

    id = models.BigIntegerField(
        primary_key=True,
        verbose_name=domain.Parent.id.title,
    )
    parent_person = models.ForeignKey(
        'persons.Person',
        verbose_name=domain.Parent.parent_person_id.title,
        max_length=domain.Parent.parent_person_id.max_length,
        db_constraint=False,
        on_delete=models.DO_NOTHING
    )
    child_person = models.ForeignKey(
        'persons.Person',
        verbose_name=domain.Parent.child_person_id.title,
        related_name='parents',
        max_length=domain.Parent.child_person_id.max_length,
        db_constraint=False,
        on_delete=models.DO_NOTHING
    )
    parent_type = models.ForeignKey(
        'parent_types.ParentType',
        verbose_name=domain.Parent.parent_type_id.title,
        db_constraint=False,
        on_delete=models.DO_NOTHING
    )
    status = models.BooleanField(
        verbose_name=domain.Parent.status.title,
        default=True
    )

    class Meta:
        db_table = 'lib_parent'
        verbose_name = 'Представитель'
        verbose_name_plural = 'Представители'
