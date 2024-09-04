import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = [
        ('lib_publishings', '0005_delete_duplicates'),
        ('lib_registry', '0045_auto_20240618_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libregistryexample',
            name='inv_number',
        ),
        migrations.AddField(
            model_name='libregistryexample',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=255, verbose_name='Номер накладной'),
        ),
        migrations.AlterField(
            model_name='libregistryexample',
            name='lib_reg_entry',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='examples',
                to='lib_registry.libregistryentry',
                verbose_name='Библиотечное издание',
            ),
        ),
        migrations.AlterField(
            model_name='libregistryexample',
            name='publishing',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='examples',
                to='lib_publishings.librarypublishings',
                verbose_name='Издательство',
            ),
        ),
    ]
