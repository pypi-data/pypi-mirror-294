from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school',
            name='person_id',
        ),
        migrations.AddField(
            model_name='school',
            name='manager',
            field=models.CharField(max_length=100, null=True, verbose_name='Директор ОО'),
        ),
    ]
