# Generated by Django 3.0.4 on 2020-05-12 18:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_auto_20200512_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estate',
            name='transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.TransactionType'),
        ),
    ]
