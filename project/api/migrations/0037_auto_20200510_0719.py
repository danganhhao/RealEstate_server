# Generated by Django 3.0.4 on 2020-05-10 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auto_20200428_0045'),
    ]

    operations = [
        # migrations.CreateModel(
        #     name='News',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('title', models.CharField(max_length=200)),
        #         ('subTitle', models.TextField(blank=True, null=True)),
        #         ('content', models.TextField(blank=True, null=True)),
        #     ],
        # ),
        # migrations.CreateModel(
        #     name='NewsType',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('name', models.CharField(max_length=50)),
        #     ],
        # ),
        migrations.AlterField(
            model_name='estate',
            name='lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='estate',
            name='lng',
            field=models.FloatField(blank=True, null=True),
        ),
        # migrations.CreateModel(
        #     name='NewsImage',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('image', models.CharField(blank=True, max_length=300, null=True)),
        #         ('description', models.CharField(blank=True, max_length=300, null=True)),
        #         ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='api.News')),
        #     ],
        # ),
        # migrations.AddField(
        #     model_name='news',
        #     name='newsType',
        #     field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.NewsType'),
        # ),
    ]
