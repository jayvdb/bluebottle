# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-14 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0002_auto_20161115_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistic',
            name='type',
            field=models.CharField(choices=[(b'manual', 'Manual'), (b'donated_total', 'Donated total'), (b'projects_online', 'Projects online'), (b'projects_realized', 'Projects realized'), (b'tasks_realized', 'Tasks realized'), (b'people_involved', 'People involved'), (b'amount_matched', 'Amount Matched'), (b'votes_cast', 'Number of votes cast')], db_index=True, default=b'manual', max_length=20, verbose_name='Type'),
        ),
    ]