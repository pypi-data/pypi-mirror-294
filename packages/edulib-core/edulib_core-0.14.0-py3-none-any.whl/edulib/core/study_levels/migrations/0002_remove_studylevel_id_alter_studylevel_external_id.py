from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('study_levels', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studylevel',
            name='id',
        ),
        migrations.AlterField(
            model_name='studylevel',
            name='external_id',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='Глобальный идентификатор'),
        ),
        migrations.RenameField(
            model_name='studylevel',
            old_name='external_id',
            new_name='id',
        ),
    ]
