import random

from django.db import migrations


def populate_slug(apps, schema_editor):

    SlugEnding = apps.get_model('slug', 'SlugEnding')

    hex_endings = []
    for i in range(0xffff):
        hex_ending = "{0:0{1}x}".format(i, 4)
        hex_endings.append(hex_ending)

    random.shuffle(hex_endings)

    for hex_ending in hex_endings:
        SlugEnding.objects.create(ending=hex_ending)


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0003_table_slug'),
    ]

    operations = [
        migrations.RunPython(populate_slug),
    ]
