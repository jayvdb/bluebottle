# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-18 08:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funding_stripe', '0004_auto_20200318_1504'),
        ('funding', '0058_auto_20201118_0954')
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentintent',
            name='donation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='funding.Donor'),
        ),
    ]