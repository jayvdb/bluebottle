# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-07-07 06:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funding_telesom', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='telesompayment',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='telesompayment',
            name='currency',
            field=models.CharField(default=b'USD', max_length=3),
        ),
    ]