# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-03 09:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0063_auto_20200915_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectimagescontent',
            name='contentitem_ptr',
        ),
        migrations.RemoveField(
            model_name='projectscontent',
            name='projects',
        ),
        migrations.DeleteModel(
            name='ProjectImagesContent',
        ),
    ]