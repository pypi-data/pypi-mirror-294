import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):
    dependencies = [
        ('readers', '0015_remove_reader_circles_remove_reader_favorite_subject_and_more'),
        ('lib_registry', '0047_alter_libexchangefund_id_and_more'),
        ('issuance_delivery', '0005_auto_20240202_0909'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuancedelivery',
            name='department',
        ),
        migrations.RemoveField(
            model_name='issuancedelivery',
            name='ex_number',
        ),
        migrations.RemoveField(
            model_name='issuancedelivery',
            name='recipient_id',
        ),
        migrations.AddField(
            model_name='issuancedelivery',
            name='extension_days_count',
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name='Количество дней на продление выдачи'
            ),
        ),
        migrations.AlterField(
            model_name='issuancedelivery',
            name='example',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='lib_registry.libregistryexample',
                verbose_name='Экземпляр издания',
            ),
        ),
        migrations.AlterField(
            model_name='issuancedelivery',
            name='fact_delivery_date',
            field=models.DateField(blank=True, null=True, verbose_name='Фактическая дата сдачи экземпляра'),
        ),
        migrations.AlterField(
            model_name='issuancedelivery',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='issuancedelivery',
            name='issuance_date',
            field=models.DateField(verbose_name='Дата выдачи экземпляра издания'),
        ),
        migrations.AlterField(
            model_name='issuancedelivery',
            name='reader',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='readers.reader',
                verbose_name='Читатель, получивший экземпляр',
            ),
        ),
        migrations.AlterField(
            model_name='issuancedelivery',
            name='special_notes',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Комментарий'),
        ),
    ]
