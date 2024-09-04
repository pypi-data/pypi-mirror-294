from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('genders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gender',
            name='id',
        ),
        migrations.AlterField(
            model_name='gender',
            name='external_id',
            field=models.CharField(max_length=36, primary_key=True, serialize=False, verbose_name='Глобальный идентификатор'),
        ),
        migrations.RenameField(
            model_name='gender',
            old_name='external_id',
            new_name='id',
        ),
    ]
