# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-12 14:19
from __future__ import unicode_literals

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0025_auto_20201016_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initiativeplatformsettings',
            name='activity_types',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('funding', 'Funding'), ('event', 'Events'), ('assignment', 'Assignment'), ('periodactivity', 'Activity during a period'), ('dateactivity', 'Activity on a specific date')], max_length=100),
        ),
    ]