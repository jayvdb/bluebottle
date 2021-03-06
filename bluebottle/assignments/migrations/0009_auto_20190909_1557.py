# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-09-09 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0008_auto_20190909_1545'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='place',
            new_name='location',
        ),
        migrations.AlterField(
            model_name='assignment',
            name='end_date',
            field=models.DateField(blank=True, help_text='Either the deadline or the date it will take place.', null=True, verbose_name='end date'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='end_date_type',
            field=models.CharField(choices=[(b'deadline', 'Deadline'), (b'on_date', 'On specific date')], default=None, help_text='Whether the end date is a deadline or a specific date the assignment takes place.', max_length=50, null=True, verbose_name='end date'),
        ),
    ]
