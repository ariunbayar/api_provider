from django.db import migrations


def create_error_types(apps, schema_editor):

    ErrorType = apps.get_model('error', 'ErrorType')

    ErrorType.objects.create(
            code='E501-1',
            summary='record.insert - Excessive columns',
            description=None,
        )

    ErrorType.objects.create(
            code='E501-2',
            summary='record.insert - Missing columns',
            description=None,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('error', '0004_auto_20191127_1508'),
    ]

    operations = [
        migrations.RunPython(create_error_types),
    ]
