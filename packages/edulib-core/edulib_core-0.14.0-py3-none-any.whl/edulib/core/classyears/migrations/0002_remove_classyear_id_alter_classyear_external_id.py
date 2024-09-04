from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('classyears', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classyear',
            name='id',
        ),
        migrations.AlterField(
            model_name='classyear',
            name='external_id',
            field=models.CharField(max_length=36, primary_key=True, serialize=False, verbose_name='Глобальный идентификатор'),
        ),
        migrations.RenameField(
            model_name='classyear',
            old_name='external_id',
            new_name='id',
        ),
    ]
