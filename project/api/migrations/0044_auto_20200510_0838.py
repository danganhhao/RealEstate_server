# Generated by Django 3.0.4 on 2020-05-10 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_auto_20200510_0836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estate',
            old_name='lat2',
            new_name='lat',
        ),
        migrations.RenameField(
            model_name='estate',
            old_name='lng2',
            new_name='lng',
        ),
    ]