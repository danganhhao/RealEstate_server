# Generated by Django 3.0.4 on 2020-04-14 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20200414_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estateimage',
            name='estate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Estate'),
        ),
    ]
