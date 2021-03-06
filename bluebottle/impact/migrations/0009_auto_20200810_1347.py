# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-08-10 11:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impact', '0008_impacttype_icon'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='impactgoal',
            options={'verbose_name': 'impact goal', 'verbose_name_plural': 'impact goals'},
        ),
        migrations.AlterModelOptions(
            name='impacttype',
            options={'verbose_name': 'impact type', 'verbose_name_plural': 'impact types'},
        ),
        migrations.RemoveField(
            model_name='impacttypetranslation',
            name='unit',
        ),
        migrations.AlterField(
            model_name='impactgoal',
            name='realized',
            field=models.FloatField(blank=True, help_text='the realised impact', null=True, verbose_name='realized'),
        ),
        migrations.AlterField(
            model_name='impactgoal',
            name='target',
            field=models.FloatField(help_text='the impact target', null=True, verbose_name='target'),
        ),
        migrations.AlterField(
            model_name='impacttype',
            name='icon',
            field=models.CharField(blank=True, choices=[(b'people', 'People'), (b'time', 'Time'), (b'money', 'Money'), (b'trees', 'Trees'), (b'animals', 'Animals'), (b'jobs', 'Jobs'), (b'co2', 'C02'), (b'water', 'Water'), (b'plastic', 'plastic'), (b'task', 'Task'), (b'task-completed', 'Task completed'), (b'event', 'Event'), (b'event-completed', 'Event completed'), (b'funding', 'Funding'), (b'funding-completed', 'Funding completed')], max_length=20, null=True, verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='impacttypetranslation',
            name='text_passed',
            field=models.CharField(help_text='E.g. "animals saved" or "people reached"', max_length=100, verbose_name='Text in past tense'),
        ),
        migrations.AlterField(
            model_name='impacttypetranslation',
            name='text_passed_with_value',
            field=models.CharField(help_text='E.g. "{} animals saved" or "{} people reached"', max_length=100, verbose_name='Text in past tense with realized  value'),
        ),
    ]
