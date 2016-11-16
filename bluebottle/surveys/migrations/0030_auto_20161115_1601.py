# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-15 15:01
from __future__ import unicode_literals

from django.db import migrations
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0029_auto_20160929_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggregateanswer',
            name='list',
            field=django_extensions.db.fields.json.JSONField(default=[], null=True),
        ),
        migrations.AlterField(
            model_name='aggregateanswer',
            name='options',
            field=django_extensions.db.fields.json.JSONField(default={}, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='specification',
            field=django_extensions.db.fields.json.JSONField(default={}, null=True),
        ),
    ]
