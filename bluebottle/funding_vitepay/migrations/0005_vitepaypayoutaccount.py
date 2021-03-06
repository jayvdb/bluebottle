# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-08-30 13:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0023_add_permissions'),
        ('funding_vitepay', '0004_auto_20190715_0739'),
    ]

    operations = [
        migrations.CreateModel(
            name='VitepayPayoutAccount',
            fields=[
                ('payoutaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='funding.PayoutAccount')),
                ('account_name', models.CharField(max_length=40)),
            ],
            options={
                'abstract': False,
            },
            bases=('funding.payoutaccount',),
        ),
    ]
