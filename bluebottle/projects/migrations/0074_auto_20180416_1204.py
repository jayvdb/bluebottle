# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-04-16 10:04


import bluebottle.utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0073_auto_20180416_1115'),
    ]

    operations = [
       migrations.AlterField(
            model_name='projectplatformsettings',
            name='facebook_at_work_url',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
    ]
