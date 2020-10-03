# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-18 21:45
from __future__ import unicode_literals

import bluebottle.utils.fields
from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderpayment',
            name='amount_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'Euro')], default='EUR', editable=False, max_length=4),
        ),
        migrations.AlterField(
            model_name='orderpayment',
            name='amount',
            field=bluebottle.utils.fields.MoneyField(currency_choices=[('EUR', 'Euro')], decimal_places=2, default=Decimal('0.0'), default_currency='EUR', max_digits=12, verbose_name='Amount'),
        ),
    ]
