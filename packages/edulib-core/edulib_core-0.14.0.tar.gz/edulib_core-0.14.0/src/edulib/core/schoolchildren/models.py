from django.db import (
    models,
)

from edulib.core.base.models import (
    BaseModel,
)

from . import (
    domain,
)


class Schoolchild(BaseModel):

    class Meta:
        verbose_name = 'Учащийся школы'
        verbose_name = 'Учащиеся школ'
        db_table = 'schoolchild'

    person_id = models.CharField(
        verbose_name=domain.Schoolchild.person_id.title,
        max_length=domain.Schoolchild.person_id.max_length,
        unique=True, db_index=True
    )
