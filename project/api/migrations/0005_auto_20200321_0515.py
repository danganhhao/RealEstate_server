# Generated by Django 3.0.4 on 2020-03-21 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200315_1102'),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.IntegerField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('prefix', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.IntegerField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('code', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.IntegerField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('prefix', models.CharField(max_length=20, null=True)),
                ('district_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.District')),
                ('province_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Province')),
            ],
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.IntegerField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100, null=True)),
                ('prefix', models.CharField(max_length=20, null=True)),
                ('district_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.District')),
                ('province_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Province')),
            ],
        ),
        migrations.AddField(
            model_name='district',
            name='province_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Province'),
        ),
    ]