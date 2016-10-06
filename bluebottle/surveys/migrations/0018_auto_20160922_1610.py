# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-22 14:10
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0017_auto_20160922_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='sub_questions',
            field=django_extensions.db.fields.json.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='response',
            name='submitted',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
