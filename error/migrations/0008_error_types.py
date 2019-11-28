from django.db import migrations


def create_error_types(apps, schema_editor):

    ErrorType = apps.get_model('error', 'ErrorType')

    ErrorType.objects.create(
            code='E900-2',
            summary='slug.utils - Unique slug exhausted',
            description=None,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('error', '0007_error_types'),
    ]

    operations = [
        migrations.RunPython(create_error_types),
    ]
