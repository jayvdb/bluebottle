# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-03-20 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0052_auto_20200205_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='funding',
            name='started',
            field=models.DateTimeField(blank=True, null=True, verbose_name='started'),
        ),
        migrations.AlterField(
            model_name='funding',
            name='deadline',
            field=models.DateTimeField(blank=True, help_text='If you enter a deadline, leave the duration field empty. This will override the duration.', null=True, verbose_name='deadline'),
        ),
        migrations.AlterField(
            model_name='funding',
            name='duration',
            field=models.PositiveIntegerField(blank=True, help_text='If you enter a duration, leave the deadline field empty for it to be automatically calculated.', null=True, verbose_name='duration'),
        ),
    ]