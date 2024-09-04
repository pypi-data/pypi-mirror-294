from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('pupils', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pupil',
            name='id',
        ),
        migrations.AlterField(
            model_name='pupil',
            name='external_id',
            field=models.CharField(max_length=36, primary_key=True, serialize=False, verbose_name='Глобальный идентификатор ФЛ'),
        ),
    ]
