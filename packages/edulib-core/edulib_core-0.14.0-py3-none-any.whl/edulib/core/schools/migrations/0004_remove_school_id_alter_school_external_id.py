from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0003_alter_school_territory_type_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='id',
        ),
        migrations.AlterField(
            model_name='school',
            name='external_id',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='Глобальный идентификатор'),
        ),
        migrations.RenameField(
            model_name='school',
            old_name='external_id',
            new_name='id',
        ),
    ]
