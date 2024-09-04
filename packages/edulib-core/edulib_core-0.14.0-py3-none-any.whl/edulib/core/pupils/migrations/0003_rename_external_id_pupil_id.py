from django.db import (
    migrations,
)


class Migration(migrations.Migration):

    dependencies = [
        ('pupils', '0002_remove_pupil_id_alter_pupil_external_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pupil',
            old_name='external_id',
            new_name='id',
        ),
    ]
