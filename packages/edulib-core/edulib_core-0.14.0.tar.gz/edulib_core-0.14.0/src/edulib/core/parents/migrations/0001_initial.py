import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('parent_types', '0002_remove_parenttype_id_alter_parenttype_external_id'),
        ('persons', '0003_remove_person_id_alter_person_external_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения')),
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='Глобальный идентификатор')),
                ('status', models.BooleanField(default=True, verbose_name='Статус')),
                ('child_person', models.ForeignKey(db_constraint=False, max_length=36, on_delete=django.db.models.deletion.DO_NOTHING, related_name='parents', to='persons.person', verbose_name='Ученик')),
                ('parent_person', models.ForeignKey(db_constraint=False, max_length=36, on_delete=django.db.models.deletion.DO_NOTHING, to='persons.person', verbose_name='Представитель')),
                ('parent_type', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, to='parent_types.parenttype', verbose_name='Тип представителя')),
            ],
            options={
                'verbose_name': 'Представитель',
                'verbose_name_plural': 'Представители',
                'db_table': 'lib_parent',
            },
        ),
    ]
