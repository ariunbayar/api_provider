from django.db import migrations


def create_error_types(apps, schema_editor):

    ErrorType = apps.get_model('error', 'ErrorType')

    ErrorType.objects.create(
            code='E404-2',
            summary='record.fetch - Table.name lookup',
            description=None,
        )

    ErrorType.objects.create(
            code='E900-1',
            summary='RecordModelFactory.value_to_jsonable - Undefined datatype',
            description=None,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('error', '0006_error_types'),
    ]

    operations = [
        migrations.RunPython(create_error_types),
    ]
