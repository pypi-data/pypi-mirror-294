import django.db.models.deletion
from django.db import (
    migrations,
    models,
)

import edulib.core.lib_registry.domain.model


class Migration(migrations.Migration):
    dependencies = [
        ('federal_books', '0001_initial'),
        ('directory', '0004_remove_catalog_index_bbc_alter_catalog_level_and_more'),
        ('lib_example_types', '0006_remove_libraryexampletype_code_and_more'),
        ('lib_registry', '0040_auto_20240205_1201'),
        ('lib_sources', '003_update_verbose_names'),
        ('lib_udc', '0007_rebuild'),
        ('parallels', '0001_initial'),
        ('lib_authors', '0003_auto_20190327_1140'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='libregistryentry',
            options={'verbose_name': 'Библиотечное издание', 'verbose_name_plural': 'Библиотечные издания'},
        ),
        migrations.RemoveField(
            model_name='libregistryentry',
            name='study_level_ids',
        ),
        migrations.AddField(
            model_name='libregistryentry',
            name='status',
            field=models.PositiveSmallIntegerField(
                choices=[(1, 'Действующие'), (2, 'Списанные')],
                default=edulib.core.lib_registry.domain.model.EntryStatus['CURRENT'],
                verbose_name='Статус',
            ),
        ),
        migrations.AddField(
            model_name='libregistryentry',
            name='federal_book',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='federal_books.federalbook',
                verbose_name='Учебник федерального перечня',
            ),
        ),
        migrations.AlterField(
            model_name='libregistryentry',
            name='age_tag',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='lib_registry.libmarkinformproduct',
                verbose_name='Знак информационной продукции',
            ),
        ),
        migrations.AlterField(
            model_name='libregistryentry',
            name='all_in_fund',
            field=models.BooleanField(default=False, verbose_name='Издание со всеми экземплярами переданы в фонд'),
        ),
        migrations.AlterField(
            model_name='libregistryentry',
            name='bbc',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='directory.catalog',
                verbose_name='Раздел ББК',
            ),
        ),
        migrations.AlterField(
            model_name='libregistryentry',
            name='discipline_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Предмет'),
        ),
        migrations.AlterField(
            model_name='libregistryentry',
            name='on_balance',
            field=models.BooleanField(default=False, verbose_name='Принято на баланс'),
        ),
        migrations.AlterField(
            model_name='libregistryentry',
            name='school_id',
            field=models.BigIntegerField(verbose_name='Организация'),
        ),
        migrations.AlterField(
            model_name='libregistryentry',
            name='short_info',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Краткое описание'),
        ),
        migrations.AlterField(
            model_name='libregistryentry',
            name='source',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='lib_sources.librarysource',
                verbose_name='Источник поступления',
            ),
        ),
        migrations.AlterField(
            model_name='libregistryentry',
            name='tags',
            field=models.CharField(blank=True, max_length=350, null=True, verbose_name='Ключевые слова'),
        ),
        migrations.AlterField(
            model_name='libregistryentry',
            name='type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='lib_example_types.libraryexampletype',
                verbose_name='Тип',
            ),
        ),
        migrations.AlterField(
            model_name='libregistryentry',
            name='udc',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='lib_udc.libraryudc',
                verbose_name='Раздел УДК',
            ),
        ),
        migrations.CreateModel(
            name='RegistryEntryParallel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
                ('modified', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения')),
                (
                    'entry',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='lib_registry.libregistryentry',
                        verbose_name='Библиотечное издание',
                    ),
                ),
                (
                    'parallel',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to='parallels.parallel', verbose_name='Параллель'
                    ),
                ),
            ],
            options={
                'verbose_name': 'Параллель библиотечного издания',
                'verbose_name_plural': 'Параллели библиотечных изданий',
            },
        ),
        migrations.AddField(
            model_name='libregistryentry',
            name='parallels',
            field=models.ManyToManyField(
                through='lib_registry.RegistryEntryParallel', to='parallels.parallel', verbose_name='Параллели'
            ),
        ),
        migrations.RenameField(
            model_name='libregistryentry',
            old_name='book_title',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='libregistryentry',
            name='title',
            field=models.CharField(max_length=350, verbose_name='Наименование'),
        ),
        migrations.AddField(
            model_name='libregistryentry',
            name='author',
            field=models.ForeignKey(
                verbose_name='Автор',
                to='lib_authors.LibraryAuthors',
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
            ),
        ),
    ]
