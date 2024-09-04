from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_units', '0003_remove_municipalunit_code_remove_municipalunit_okato'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='municipalunit',
            name='id',
        ),
        migrations.AlterField(
            model_name='municipalunit',
            name='external_id',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='Глобальный идентификатор'),
        ),
        migrations.RenameField(
            model_name='municipalunit',
            old_name='external_id',
            new_name='id',
        ),
    ]
