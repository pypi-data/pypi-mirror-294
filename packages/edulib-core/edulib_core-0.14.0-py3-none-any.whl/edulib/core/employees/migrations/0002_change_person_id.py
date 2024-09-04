import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = [
        ('employees', '0001_initial'),
        ('persons', '0002_alter_person_snils'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='person_id',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='persons.person',
                verbose_name='Физлицо',
            ),
        ),
        migrations.RenameField('employee', 'person_id', 'person'),
    ]
