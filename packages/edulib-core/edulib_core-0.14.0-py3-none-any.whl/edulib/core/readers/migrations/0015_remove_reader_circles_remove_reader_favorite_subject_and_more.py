from django.db import (
    migrations,
    models,
)

import edulib.core.readers.domain.model


class Migration(migrations.Migration):
    dependencies = [
        ('readers', '0014_auto_20240202_0917'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reader',
            name='circles',
        ),
        migrations.RemoveField(
            model_name='reader',
            name='favorite_subject',
        ),
        migrations.RemoveField(
            model_name='reader',
            name='hobby',
        ),
        migrations.RemoveField(
            model_name='reader',
            name='is_read',
        ),
        migrations.RemoveField(
            model_name='reader',
            name='other_libs',
        ),
        migrations.RemoveField(
            model_name='reader',
            name='reading_about',
        ),
        migrations.RemoveField(
            model_name='reader',
            name='tech',
        ),
        migrations.AlterField(
            model_name='reader',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='role',
            field=models.SmallIntegerField(
                choices=[(1, 'Ученик'), (2, 'Сотрудник'), (3, 'Все')],
                default=edulib.core.readers.domain.model.ReaderRole['STUDENT'],
                verbose_name='Роль',
            ),
        ),
        migrations.AlterField(
            model_name='reader',
            name='school_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Образовательная организация'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='schoolchild_id',
            field=models.BigIntegerField(blank=True, null=True, unique=True, verbose_name='Учащийся'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='teacher_id',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='reader2response',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='searchrequesthistory',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='teacherreview',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
