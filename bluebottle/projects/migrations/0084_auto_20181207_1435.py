# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-12-07 13:35
from __future__ import unicode_literals

import bluebottle.utils.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0083_auto_20181129_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='bank_details_reviewed',
        ),
        migrations.AlterField(
            model_name='projectcreatetemplate',
            name='default_amount_asked',
            field=bluebottle.utils.fields.MoneyField(blank=True, currency_choices="[('EUR', u'Euro')]", decimal_places=2, default=None, max_digits=12, null=True),
        ),
    ]
