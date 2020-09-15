# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-07-08 12:17


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0014_auto_20190628_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initiative',
            name='promoter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='promoter'),
        ),
    ]
