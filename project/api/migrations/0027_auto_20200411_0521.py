# Generated by Django 3.0.4 on 2020-04-11 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20200411_0455'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FilterType',
            new_name='FilterMaxPrice',
        ),
    ]