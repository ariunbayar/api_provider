from django.db import migrations


def create_error_types(apps, schema_editor):

    ErrorType = apps.get_model('error', 'ErrorType')

    ErrorType.objects.create(
            code='E101-1',
            summary='record.insert - Invalid boolean value',
            description=None,
        )

    ErrorType.objects.create(
            code='E101-2',
            summary='record.insert - Invalid integer value',
            description=None,
        )

    ErrorType.objects.create(
            code='E001-1',
            summary='record.insert - Integer bound exceeds -0x80000000 and 0x7fffffff',
            description=None,
        )

    ErrorType.objects.create(
            code='E101-3',
            summary='record.insert - Char250 max length',
            description=None,
        )

    ErrorType.objects.create(
            code='E101-4',
            summary='record.insert - Invalid datetime',
            description=None,
        )

    ErrorType.objects.create(
            code='E501-3',
            summary='record.insert - Could not create object',
            description=None,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('error', '0005_error_type_e501-1_e501-2'),
    ]

    operations = [
        migrations.RunPython(create_error_types),
    ]
