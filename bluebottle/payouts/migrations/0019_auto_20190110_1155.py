# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-01-10 10:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bb_payouts', '0003_auto_20190110_1155'),
        ('payouts', '0018_auto_20190108_0858'),
        ('payouts_dorado', '0001_initial')
    ]

    operations = [
        migrations.DeleteModel(
            name='OrganizationPayout',
        ),
        migrations.RemoveField(
            model_name='projectpayout',
            name='project',
        ),
        migrations.DeleteModel(
            name='ProjectPayout',
        ),
    ]