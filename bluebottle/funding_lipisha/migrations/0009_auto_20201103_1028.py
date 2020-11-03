# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-03 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funding_lipisha', '0008_lipishabankaccount_mpesa_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lipishapaymentprovider',
            name='paybill',
            field=models.CharField(help_text=b'Find this at https://app.lypa.io/payment under `Business Number`', max_length=10, verbose_name='Business Number'),
        ),
    ]
