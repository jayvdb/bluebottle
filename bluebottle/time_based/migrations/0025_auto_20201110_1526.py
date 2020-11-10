# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-10 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0027_contributionvalue'),
        ('impact', '0017_auto_20201110_1526'),
        ('cms', '0064_auto_20201110_1526'),
        ('time_based', '0024_auto_20201103_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ongoingactivity',
            name='timebasedactivity_ptr',
        ),
        migrations.AlterField(
            model_name='withadeadlineactivity',
            name='duration_period',
            field=models.CharField(blank=True, choices=[('overall', 'overall'), ('days', 'per day'), ('weeks', 'per week'), ('months', 'per month')], max_length=20, null=True, verbose_name='duration period'),
        ),
        migrations.DeleteModel(
            name='OngoingActivity',
        ),
    ]
