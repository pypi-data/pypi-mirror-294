from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='snils',
            field=models.CharField(blank=True, db_index=True, default='', max_length=14, null=True, verbose_name='СНИЛС'),
        ),
    ]
