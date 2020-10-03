# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-11-06 11:06
from __future__ import unicode_literals
from itertools import groupby

from django.db import migrations


def create_payouts(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')
    Funding = apps.get_model('funding', 'Funding')
    Payout = apps.get_model('funding', 'Payout')
    Donation = apps.get_model('funding', 'Donation')
    LegacyPayment = apps.get_model('funding', 'LegacyPayment')

    def get_currency_and_provider(donation):
        return (
            donation.amount.currency,
            donation.payment.polymorphic_ctype.model.replace('payment', '').replace('source' ,'')
        )


    for project in Project.objects.exclude(payout_status__isnull=True):
        funding = Funding.objects.get(pk=project.funding_id)

        for (currency, provider), donations in groupby(
            Donation.objects.select_related('payment', 'payment__polymorphic_ctype').filter(activity=funding, status='succeeded', payment__isnull=False),
            lambda x: get_currency_and_provider(x)
        ):
            payout = Payout.objects.create(
                status=project.payout_status,
                activity=funding,
                provider=provider,
                currency=currency
            )
            Donation.objects.filter(
                pk__in=[donation.pk for donation in donations]
            ).update(payout=payout)


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0092_auto_20191031_0901'),
    ]

    operations = [
        #migrations.RunPython(create_payouts)
    ]
