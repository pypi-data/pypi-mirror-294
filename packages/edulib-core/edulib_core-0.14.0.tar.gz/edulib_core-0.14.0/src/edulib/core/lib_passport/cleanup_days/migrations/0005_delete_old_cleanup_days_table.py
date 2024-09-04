import django.db.models.deletion
from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('cleanup_days', '0004_migrate_cleanup_days_data'),
        ('lib_passport', '0019_remove_from_lib_passport_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LibPassportCleanupDays',
        ),
        migrations.AlterField(
            model_name='cleanupdays',
            name='lib_passport',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cleanup_days', to='lib_passport.libpassport', verbose_name='Паспорт библиотеки'),
        ),
    ]
