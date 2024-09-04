from django.db import (
    migrations,
)


def forwards(apps, schema_editor):
    CleanupDays = apps.get_model('cleanup_days', 'CleanupDays')
    LibPassportCleanupDays = apps.get_model('cleanup_days', 'LibPassportCleanupDays')
    LibPassport = apps.get_model('lib_passport', 'LibPassport')

    for old_day in LibPassportCleanupDays.objects.all():
        try:
            lib_passport = LibPassport.objects.get(school_id=old_day.school_id)
            new_day = CleanupDays(
                lib_passport_id=lib_passport.id,
                cleanup_date=old_day.cleanup_date
            )
            new_day.save()
        except LibPassport.DoesNotExist:
            print(f"LibPassport with school_id={old_day.school_id} does not exist.")


def backwards(apps, schema_editor):
    CleanupDays = apps.get_model('cleanup_days', 'CleanupDays')
    LibPassportCleanupDays = apps.get_model('lib_passport', 'LibPassportCleanupDays')

    for new_day in CleanupDays.objects.all():
        old_day = LibPassportCleanupDays(
            school_id=new_day.lib_passport.school_id,
            cleanup_date=new_day.cleanup_date
        )
        old_day.save()


class Migration(migrations.Migration):

    dependencies = [
        ('lib_passport', '0018_data_migration_for_work_mode_and_address'),
        ('cleanup_days', '0003_create_new_table_for_cleanup_day'),


    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
