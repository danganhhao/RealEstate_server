# Generated by Django 3.0.4 on 2020-04-14 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_filterarea_filterminprice_filternumberofroom_filterposttime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estateimage',
            name='image',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]