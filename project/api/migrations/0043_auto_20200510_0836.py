# Generated by Django 3.0.4 on 2020-05-10 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_auto_20200510_0813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estate',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='estate',
            name='lng',
        ),
    ]