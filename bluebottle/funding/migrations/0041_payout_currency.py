# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-10-29 12:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0040_auto_20191029_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='payout',
            name='currency',
            field=models.CharField(default='EUR', max_length=5),
            preserve_default=False,
        ),
    ]
