import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('cleanup_days', '0002_auto_20180420_0941'),
        ('lib_passport', '0017_create_work_mode'),
    ]

    operations = [
        migrations.CreateModel(
            name='CleanupDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cleanup_date', models.DateField(verbose_name='Дата санитарного дня')),
                ('lib_passport', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='temp_cleanup_days', to='lib_passport.libpassport', verbose_name='Паспорт библиотеки')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Дата создания')),
                ('modified', models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Дата изменения')),
            ],
            options={
                'db_table': 'cleanup_days',
                'verbose_name': 'Санитарные дни',
                'verbose_name_plural': 'Санитарные дни',
            },
        ),
    ]
