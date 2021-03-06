# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-01-24 11:30
from __future__ import unicode_literals
from django.db.models import F

from django.db import migrations


def set_payout_amount(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Donation = apps.get_model('funding', 'Donation')
    Donation.objects.update(
        payout_amount=F('amount'),
        payout_amount_currency=F('amount_currency')
    )


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0049_auto_20200124_1032'),
    ]

    operations = [
        migrations.RunPython(set_payout_amount)
    ]
