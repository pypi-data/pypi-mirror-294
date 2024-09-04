from django.db import (
    migrations,
    models,
)


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0002_remove_school_person_id_school_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='territory_type_id',
            field=models.BigIntegerField(null=True, verbose_name='Тип территории'),
        ),
    ]
