# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-26 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('time_based', '0037_auto_20201126_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='timebasedactivity',
            name='preparation',
            field=models.DurationField(blank=True, null=True, verbose_name='Time required for preparation'),
        ),
    ]