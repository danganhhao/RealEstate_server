# Generated by Django 3.0.4 on 2020-03-25 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20200317_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pin',
            field=models.IntegerField(default=0),
        ),
    ]