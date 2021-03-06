# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-07-10 09:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impact', '0004_auto_20200624_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='impacttypetranslation',
            name='text',
            field=models.CharField(blank=True, help_text='E.g. "save animals" or "reach people"', max_length=100, verbose_name='Text'),
        ),
        migrations.AddField(
            model_name='impacttypetranslation',
            name='text_passed',
            field=models.CharField(blank=True, help_text='E.g. "animals saved" or "people reached"', max_length=100, verbose_name='Text in passed tense'),
        ),
        migrations.AddField(
            model_name='impacttypetranslation',
            name='text_passed_with_value',
            field=models.CharField(blank=True, help_text='E.g. "{} animals saved" or "{} people reached"', max_length=100, verbose_name='Text in passed tense with realized  value'),
        ),
        migrations.AddField(
            model_name='impacttypetranslation',
            name='text_with_target',
            field=models.CharField(blank=True, help_text='E.g. "save {} animals" or "reach {} people"', max_length=100, verbose_name='Text including target'),
        ),
        migrations.AlterField(
            model_name='impacttypetranslation',
            name='unit',
            field=models.CharField(blank=True, help_text='E.g. "liters of water" or "people"', max_length=100, verbose_name='unit'),
        ),
    ]
