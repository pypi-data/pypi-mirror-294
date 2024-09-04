from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('academic_years', '0002_alter_academicyear_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='academicyear',
            name='id',
        ),
        migrations.AlterField(
            model_name='academicyear',
            name='external_id',
            field=models.CharField(max_length=36, primary_key=True, serialize=False, verbose_name='Глобальный идентификатор'),
        ),
        migrations.RenameField(
            model_name='academicyear',
            old_name='external_id',
            new_name='id',
        ),
    ]
