import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = [
        ('lib_authors', '0003_auto_20190327_1140'),
        ('lib_registry', '0042_auto_20240529_0519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libregistryentry',
            name='authors',
        ),
        migrations.AlterField(
            model_name='libregistryentry',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='lib_authors.libraryauthors',
                verbose_name='Автор',
            ),
        ),
    ]
