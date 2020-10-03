# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-17 10:37
from __future__ import unicode_literals

import bluebottle.files.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0008_auto_20201117_1137'),
        ('activities', '0030_auto_20201117_1137'),
        ('time_based', '0030_merge_20201113_1124'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OnADateApplication',
            new_name='DateParticipant'
        ),
        migrations.RenameModel(
            old_name='PeriodApplication',
            new_name='PeriodParticipant',
        ),
    ]