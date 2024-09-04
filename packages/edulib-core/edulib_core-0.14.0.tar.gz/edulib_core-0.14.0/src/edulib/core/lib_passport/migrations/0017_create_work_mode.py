import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
        ('academic_years', '0001_initial'),
        ('employees', '0002_change_person_id'),
        ('cleanup_days', '0002_auto_20180420_0941'),
        ('lib_passport', '0016_auto_20240202_0910'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lib_passport', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='work_mode', to='lib_passport.libpassport', verbose_name='Паспорт библиотеки')),
                ('schedule_mon_from', models.CharField(max_length=10, null=True, blank=True, verbose_name='Режим работы с - Понедельник')),
                ('schedule_mon_to', models.CharField(max_length=10, null=True, blank=True, verbose_name='Режим работы по - Понедельник')),
                ('schedule_tue_from', models.CharField(max_length=10, null=True, blank=True, verbose_name='Режим работы с - Вторник')),
                ('schedule_tue_to', models.CharField(max_length=10, null=True, blank=True, verbose_name='Режим работы по - Вторник')),
                ('schedule_wed_from', models.CharField(max_length=10, null=True, blank=True, verbose_name='Режим работы с - Среда')),
                ('schedule_wed_to', models.CharField(max_length=10, null=True, blank=True, verbose_name='Режим работы по - Среда')),
                ('schedule_thu_from', models.CharField(max_length=10, null=True, blank=True, verbose_name='Режим работы с - Четверг')),
                ('schedule_thu_to', models.CharField(max_length=10, null=True, blank=True, verbose_name='Режим работы по - Четверг')),
                ('schedule_fri_from', models.CharField(max_length=10, null=True, blank=True, verbose_name='Режим работы с - Пятница')),
                ('schedule_fri_to', models.CharField(max_length=10, null=True, blank=True, verbose_name='Режим работы по - Пятница')),
                ('schedule_sat_from', models.CharField(max_length=10, null=True, blank=True, verbose_name='Режим работы с - Суббота')),
                ('schedule_sat_to', models.CharField(max_length=10, null=True, blank=True, verbose_name='Режим работы по - Суббота')),
                ('schedule_sun_from', models.CharField(max_length=10, null=True, blank=True, verbose_name='Режим работы с - Воскресенье')),
                ('schedule_sun_to', models.CharField(max_length=10, null=True, blank=True, verbose_name='Режим работы по - Воскресенье')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Дата создания')),
                ('modified', models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Дата изменения')),
            ],
            options={
                'db_table': 'library_work_mode',
                'verbose_name': 'Режим работы библиотеки',
                'verbose_name_plural': 'Режим работы библиотек',
            },
        ),
        migrations.AddField(
            model_name='libpassport',
            name='address',
            field=models.ForeignKey(blank=True, null=True, db_constraint=False, on_delete=models.DO_NOTHING, to='address.address', verbose_name='Идентификатор адреса'),
        ),
        migrations.RenameField(
            model_name='libpassport',
            old_name='period_id',
            new_name='academic_year',
        ),
        migrations.AlterField(
            model_name='libpassport',
            name='academic_year',
            field=models.ForeignKey(verbose_name='Период обучения', db_constraint=False, to='academic_years.AcademicYear', on_delete=models.DO_NOTHING, null=True, blank=True,),
        ),
        migrations.RenameField(
            model_name='libpassport',
            old_name='library_chief_id',
            new_name='library_chief',
        ),
        migrations.AlterField(
            model_name='libpassport',
            name='library_chief',
            field=models.ForeignKey(verbose_name='Заведующий библиотекой', to='employees.Employee', on_delete=models.DO_NOTHING, null=True, blank=True, db_constraint=False,),
        ),
    ]
