from django.db import (
    migrations,
)


class Migration(migrations.Migration):

    dependencies = [
        ('municipal_units', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='municipalunit',
            name='parent',
        ),
    ]
