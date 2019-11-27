from django.db import migrations


def create_error_type(apps, schema_editor):
    ErrorType = apps.get_model('error', 'ErrorType')
    et = ErrorType()
    et.name = 'E404-1'
    et.summary = 'record.insert - Table.name lookup'
    et.description = None
    et.save()


class Migration(migrations.Migration):

    dependencies = [
        ('error', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_error_type),
    ]
