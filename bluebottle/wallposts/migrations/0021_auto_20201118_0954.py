# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-18 08:54
from __future__ import unicode_literals

import bluebottle.utils.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallposts', '0020_auto_20191017_2208'),
        ('funding', '0058_auto_20201118_0954')
    ]

    operations = [
        migrations.AlterField(
            model_name='wallpost',
            name='donation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wallpost', to='funding.Donor', verbose_name='Donor'),
        ),
    ]