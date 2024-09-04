from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = [
        ('academic_years', '0004_auto_20240808_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='academicyear',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False, verbose_name='Глобальный идентификатор'),
        ),
    ]
