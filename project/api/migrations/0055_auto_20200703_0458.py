# Generated by Django 3.0.4 on 2020-07-03 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0054_auto_20200702_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernotitoken',
            name='token',
            field=models.CharField(max_length=500),
        ),
    ]