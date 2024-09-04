from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('pupils', '0003_rename_external_id_pupil_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pupil',
            name='class_year_id',
            field=models.CharField(max_length=36, verbose_name='Учебный класс'),
        ),
    ]
