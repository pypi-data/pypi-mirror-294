from django.db import (
    migrations,
)
from django.db.models import (
    F,
    Q,
)


def forwards(apps, schema_editor):
    LibRegistryExample = apps.get_model('lib_registry', 'LibRegistryExample')

    LibRegistryExample.objects.filter(Q(card_number__isnull=True) | Q(card_number='')).update(
        card_number=F('inv_number')
    )


class Migration(migrations.Migration):
    dependencies = [
        ('lib_registry', '0044_alter_libregistryexample_options_and_more'),
    ]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
