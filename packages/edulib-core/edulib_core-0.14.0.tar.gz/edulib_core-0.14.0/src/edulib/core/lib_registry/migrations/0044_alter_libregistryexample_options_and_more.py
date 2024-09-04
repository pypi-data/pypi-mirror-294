import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = [
        ('lib_registry', '0043_remove_libregistryentry_authors_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='libregistryexample',
            options={
                'verbose_name': 'Экземпляр библиотечного издания',
                'verbose_name_plural': 'Экземпляры библиотечных изданий',
            },
        ),
        migrations.RemoveField(
            model_name='libregistryexample',
            name='act_date',
        ),
        migrations.RemoveField(
            model_name='libregistryexample',
            name='act_number',
        ),
        migrations.RemoveField(
            model_name='libregistryexample',
            name='employee_fullname',
        ),
        migrations.RemoveField(
            model_name='libregistryexample',
            name='employee_phone',
        ),
        migrations.RemoveField(
            model_name='libregistryexample',
            name='library',
        ),
        migrations.RemoveField(
            model_name='libregistryexample',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='libregistryexample',
            name='pub_office',
        ),
        migrations.AlterField(
            model_name='libregistryexample',
            name='book_code',
            field=models.CharField(max_length=22, verbose_name='Шифр'),
        ),
        migrations.AlterField(
            model_name='libregistryexample',
            name='card_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер карточки учёта'),
        ),
        migrations.AlterField(
            model_name='libregistryexample',
            name='duration',
            field=models.CharField(max_length=10, verbose_name='Количество страниц / длительность'),
        ),
        migrations.AlterField(
            model_name='libregistryexample',
            name='edition',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Издание'),
        ),
        migrations.AlterField(
            model_name='libregistryexample',
            name='edition_place',
            field=models.CharField(max_length=50, verbose_name='Место издания'),
        ),
        migrations.AlterField(
            model_name='libregistryexample',
            name='edition_year',
            field=models.PositiveSmallIntegerField(verbose_name='Год издания'),
        ),
        migrations.AlterField(
            model_name='libregistryexample',
            name='fin_source',
            field=models.SmallIntegerField(
                blank=True,
                choices=[
                    (0, 'Федеральный бюджет'),
                    (1, 'Региональный бюджет'),
                    (2, 'Муниципальный бюджет'),
                    (3, 'Средства организации'),
                    (4, 'Средства спонсоров'),
                ],
                null=True,
                verbose_name='Источник финансирования',
            ),
        ),
        migrations.AlterField(
            model_name='libregistryexample',
            name='inflow_date',
            field=models.DateField(verbose_name='Дата поступления'),
        ),
        migrations.AlterField(
            model_name='libregistryexample',
            name='lib_reg_entry',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='lib_registry.libregistryentry',
                verbose_name='Библиотечное издание',
            ),
        ),
        migrations.AlterField(
            model_name='libregistryexample',
            name='max_date',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='Максимальный срок выдачи'),
        ),
        migrations.AlterField(
            model_name='libregistryexample',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='Стоимость'),
        ),
    ]
