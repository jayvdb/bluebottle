# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-03-11 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_pub', '0005_auto_20200311_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activitypubplatformsettings',
            name='public_key',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='activitypubplatformsettings',
            name='secret_key',
            field=models.TextField(),
        ),
    ]
