from django.db import (
    migrations,
)
from django.db.models import (
    F,
)


def forwards(apps, schema_editor):
    LibRegistryEntry = apps.get_model('lib_registry', 'LibRegistryEntry')
    LibraryAuthors = apps.get_model('lib_authors', 'LibraryAuthors')

    for entry in LibRegistryEntry.objects.iterator():
        author = LibraryAuthors.objects.filter(name__iexact=entry.authors.strip()).first()
        if not author:
            author = LibraryAuthors.objects.create(name=entry.authors.strip())
        entry.author = author
        entry.save()


def backwards(apps, schema_editor):
    LibRegistryEntry = apps.get_model('lib_registry', 'LibRegistryEntry')

    for entry in LibRegistryEntry.objects.annotate(author_name=F('author__name')).iterator():
        entry.authors = entry.author_name
        entry.save()


class Migration(migrations.Migration):
    dependencies = [
        ('lib_registry', '0041_alter_libregistryentry_options_and_more'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
