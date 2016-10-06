# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-19 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_auto_20160829_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[(b'open', 'Open'), (b'in progress', 'Running'), (b'realized', 'Realised'), (b'closed', 'Closed')], default=b'open', max_length=20, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='taskmember',
            name='status',
            field=models.CharField(choices=[(b'applied', 'Applied'), (b'accepted', 'Accepted'), (b'rejected', 'Rejected'), (b'stopped', 'Withdrew'), (b'realized', 'Realised')], default=b'applied', max_length=20, verbose_name='status'),
        ),
    ]
