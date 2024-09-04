import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20240119_1121'),
        ('lib_passport', '0019_remove_from_lib_passport_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='libpassportdocuments',
            name='library_passport',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='lib_passport.libpassport', verbose_name='Идентификатор паспорта библиотеки'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='libpassportdocuments',
            name='doc_type',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Нормативно-правовая база'), (2, 'Документы учета работы библиотеки')], null=True, verbose_name='Тип документа'),
        ),
        migrations.AlterField(
            model_name='libpassportdocuments',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
