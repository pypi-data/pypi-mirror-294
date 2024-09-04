from django.db import (
    migrations,
)


def forwards(apps, schema_editor):
    LibPassport = apps.get_model('lib_passport', 'LibPassport')
    WorkMode = apps.get_model('lib_passport', 'WorkMode')
    Address = apps.get_model('address', 'Address')

    for passport in LibPassport.objects.all():
        if any([
            passport.shedule_mon_from,
            passport.shedule_mon_to,
            passport.shedule_tue_from,
            passport.shedule_tue_to,
            passport.shedule_wed_from,
            passport.shedule_wed_to,
            passport.shedule_thu_from,
            passport.shedule_thu_to,
            passport.shedule_fri_from,
            passport.shedule_fri_to,
            passport.shedule_sat_from,
            passport.shedule_sat_to,
            passport.shedule_sun_from,
            passport.shedule_sun_to,
        ]):
            work_mode = WorkMode.objects.create(
                lib_passport=passport,
                schedule_mon_from=passport.shedule_mon_from,
                schedule_mon_to=passport.shedule_mon_to,
                schedule_tue_from=passport.shedule_tue_from,
                schedule_tue_to=passport.shedule_tue_to,
                schedule_wed_from=passport.shedule_wed_from,
                schedule_wed_to=passport.shedule_wed_to,
                schedule_thu_from=passport.shedule_thu_from,
                schedule_thu_to=passport.shedule_thu_to,
                schedule_fri_from=passport.shedule_fri_from,
                schedule_fri_to=passport.shedule_fri_to,
                schedule_sat_from=passport.shedule_sat_from,
                schedule_sat_to=passport.shedule_sat_to,
                schedule_sun_from=passport.shedule_sun_from,
                schedule_sun_to=passport.shedule_sun_to,
            )
        if any([
            passport.f_address_place,
            passport.f_address_street,
            passport.f_address_house,
            passport.f_address_house_guid,
            passport.f_address_corps,
            passport.f_address_full,
            passport.f_address_zipcode,
        ]):
            address = Address.objects.create(
                place=passport.f_address_place,
                street=passport.f_address_street,
                house_num=passport.f_address_house,
                house=passport.f_address_house_guid,
                house_corps=passport.f_address_corps,
                full=passport.f_address_full,
                zip_code=passport.f_address_zipcode,
            )
            passport.address = address

        if passport.address:
            passport.save()


def backwards(apps, schema_editor):
    LibPassport = apps.get_model('lib_passport', 'LibPassport')
    WorkMode = apps.get_model('lib_passport', 'WorkMode')
    Address = apps.get_model('address', 'Address')

    for passport in LibPassport.objects.all():
        work_mode = WorkMode.objects.filter(lib_passport=passport).first()
        if work_mode:
            passport.shedule_mon_from = passport.work_mode.schedule_mon_from
            passport.shedule_mon_to = passport.work_mode.schedule_mon_to
            passport.shedule_tue_from = passport.work_mode.schedule_tue_from
            passport.shedule_tue_to = passport.work_mode.schedule_tue_to
            passport.shedule_wed_from = passport.work_mode.schedule_wed_from
            passport.shedule_wed_to = passport.work_mode.schedule_wed_to
            passport.shedule_thu_from = passport.work_mode.schedule_thu_from
            passport.shedule_thu_to = passport.work_mode.schedule_thu_to
            passport.shedule_fri_from = passport.work_mode.schedule_fri_from
            passport.shedule_fri_to = passport.work_mode.schedule_fri_to
            passport.shedule_sat_from = passport.work_mode.schedule_sat_from
            passport.shedule_sat_to = passport.work_mode.schedule_sat_to
            passport.shedule_sun_from = passport.work_mode.schedule_sun_from
            passport.shedule_sun_to = passport.work_mode.schedule_sun_to
            work_mode.delete()

        if passport.address:
            passport.f_address_place = passport.address.place
            passport.f_address_street = passport.address.street
            passport.f_address_house = passport.address.house_num
            passport.f_address_house_guid = passport.address.house
            passport.f_address_corps = passport.address.house_corps
            passport.f_address_full = passport.address.full
            passport.f_address_zipcode = passport.address.zip_code
            Address.objects.filter(id=passport.address_id).delete()
            passport.address = None

        passport.save()


class Migration(migrations.Migration):

    dependencies = [
        ('lib_passport', '0017_create_work_mode'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
