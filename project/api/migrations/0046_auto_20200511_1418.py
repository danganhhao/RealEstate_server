# Generated by Django 3.0.4 on 2020-05-11 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_estate_isapproved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estate',
            name='isApproved',
            field=models.IntegerField(default=0),
        ),
    ]