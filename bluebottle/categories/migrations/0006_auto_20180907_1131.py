# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-07 09:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0005_auto_20180117_0924'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['title'], 'permissions': (('api_read_category', 'Can view categories through API'),), 'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
    ]