# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-02 08:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_auto_20160802_1025'),
    ]

    operations = [
        migrations.RunSQL('update tasks_task set deadline=(deadline::date || \' 23:59:59\')::timestamp AT TIME ZONE \'UTC\';')
    ]
