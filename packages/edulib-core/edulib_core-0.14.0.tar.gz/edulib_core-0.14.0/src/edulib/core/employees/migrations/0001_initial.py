from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения')),
                ('external_id', models.BigIntegerField(db_index=True, verbose_name='Глобальный идентификатор')),
                ('person_id', models.BigIntegerField(verbose_name='Физлицо')),
                ('school_id', models.BigIntegerField(verbose_name='Организация')),
                ('info_date_begin', models.DateField(verbose_name='Дата вступления в должность')),
                ('info_date_end', models.DateField(null=True, verbose_name='Дата выхода из должности')),
                ('personnel_num', models.CharField(max_length=100, null=True, verbose_name='Табельный номер')),
                ('job_code', models.BigIntegerField(null=True, verbose_name='Код должности')),
                ('job_name', models.CharField(max_length=200, null=True, verbose_name='Наименование должности')),
                ('employment_kind_id', models.BigIntegerField(verbose_name='Вид занятости')),
                ('object_status', models.BooleanField(verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
                'db_table': 'employee',
            },
        ),
    ]
