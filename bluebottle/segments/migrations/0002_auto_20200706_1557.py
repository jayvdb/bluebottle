# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-07-06 13:57


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('segments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SegmentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
            ],
        ),
        migrations.AlterField(
            model_name='segment',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='segment',
            name='type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='segments', to='segments.SegmentType', verbose_name='type'),
            preserve_default=False,
        ),
    ]
