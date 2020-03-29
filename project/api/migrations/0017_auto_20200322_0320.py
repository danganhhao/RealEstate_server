# Generated by Django 3.0.4 on 2020-03-22 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20200322_0305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='street',
            name='district_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='streets', to='api.District'),
        ),
        migrations.AlterField(
            model_name='street',
            name='province_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='streets', to='api.Province'),
        ),
        migrations.AlterField(
            model_name='ward',
            name='district_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wards', to='api.District'),
        ),
        migrations.AlterField(
            model_name='ward',
            name='province_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wards', to='api.Province'),
        ),
    ]