# Generated by Django 3.0.4 on 2020-03-21 07:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20200321_0516'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estate',
            name='location',
        ),
        migrations.AddField(
            model_name='estate',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.District'),
        ),
        migrations.AddField(
            model_name='estate',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Province'),
        ),
        migrations.AddField(
            model_name='estate',
            name='street',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Street'),
        ),
        migrations.AddField(
            model_name='estate',
            name='ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Ward'),
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
