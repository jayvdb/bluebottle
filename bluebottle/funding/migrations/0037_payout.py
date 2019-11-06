# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-10-09 15:26
from __future__ import unicode_literals

import bluebottle.fsm
import bluebottle.utils.fields
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0036_auto_20191004_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', bluebottle.fsm.FSMField(default=b'new', max_length=20)),
                ('amount_donated_currency', djmoney.models.fields.CurrencyField(choices=[(b'EUR', b'Euro')], default=b'EUR', editable=False, max_length=3)),
                ('amount_donated', bluebottle.utils.fields.MoneyField(currency_choices=[(b'EUR', b'Euro')], decimal_places=2, default=Decimal('0.0'), default_currency=b'EUR', max_digits=12, verbose_name='amount donated')),
                ('amount_pledged_currency', djmoney.models.fields.CurrencyField(choices=[(b'EUR', b'Euro')], default=b'EUR', editable=False, max_length=3)),
                ('amount_pledged', bluebottle.utils.fields.MoneyField(currency_choices=[(b'EUR', b'Euro')], decimal_places=2, default=Decimal('0.0'), default_currency=b'EUR', max_digits=12, verbose_name='amount pledged')),
                ('amount_matched_currency', djmoney.models.fields.CurrencyField(choices=[(b'EUR', b'Euro')], default=b'EUR', editable=False, max_length=3)),
                ('amount_matched', bluebottle.utils.fields.MoneyField(currency_choices=[(b'EUR', b'Euro')], decimal_places=2, default=Decimal('0.0'), default_currency=b'EUR', max_digits=12, verbose_name='amount matched')),
                ('date_approved', models.DateTimeField(blank=True, null=True, verbose_name='approved')),
                ('date_started', models.DateTimeField(blank=True, null=True, verbose_name='started')),
                ('date_completed', models.DateTimeField(blank=True, null=True, verbose_name='completed')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payout', to='funding.Funding', verbose_name='activity')),
            ],
            options={
                'verbose_name': 'payout',
                'verbose_name_plural': 'payout',
            },
            bases=(bluebottle.fsm.TransitionsMixin, models.Model),
        ),
    ]