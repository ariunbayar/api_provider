# Generated by Django 2.2.7 on 2019-11-27 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('error', '0003_auto_20191127_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errortype',
            name='code',
            field=models.CharField(db_index=True, max_length=10, unique=True),
        ),
    ]
