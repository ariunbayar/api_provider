# Generated by Django 2.2.7 on 2019-11-28 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0002_auto_20191123_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='slug',
            field=models.SlugField(allow_unicode=True, null=True),
        ),
    ]
