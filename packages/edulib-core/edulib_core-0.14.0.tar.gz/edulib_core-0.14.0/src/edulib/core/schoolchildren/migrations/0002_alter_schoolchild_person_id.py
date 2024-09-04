from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('schoolchildren', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolchild',
            name='person_id',
            field=models.CharField(db_index=True, max_length=36, unique=True, verbose_name='Физлицо'),
        ),
    ]
