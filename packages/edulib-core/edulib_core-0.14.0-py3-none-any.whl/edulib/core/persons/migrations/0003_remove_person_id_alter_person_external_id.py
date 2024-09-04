from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_alter_person_snils'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='id',
        ),
        migrations.AlterField(
            model_name='person',
            name='external_id',
            field=models.CharField(max_length=36, primary_key=True, serialize=False, verbose_name='Глобальный идентификатор ФЛ'),
        ),
        migrations.RenameField(
            model_name='person',
            old_name='external_id',
            new_name='id',
        ),
    ]
