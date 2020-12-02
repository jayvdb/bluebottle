# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-12-02 09:44
from __future__ import unicode_literals

from django.db import migrations, connection


def insert(table, fields, values):

    with connection.cursor() as cursor:
        query = 'INSERT into {} ({})  VALUES ({})'.format(
            table,
            ", ".join('"{}"'.format(field) for field in fields),
            ','.join('%s' for field in fields)
        )
        actual_values = []

        for value in values:
            actual_values.append(
                [value[field] for field in fields ]
            )

        cursor.executemany(query, actual_values)


def create_money_contributions(apps, schema_editor):
    Donor = apps.get_model('funding', 'Donor')
    Contribution = apps.get_model('activities', 'Contribution')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    MoneyContribution = apps.get_model('funding', 'MoneyContribution')

    money_contribution_ctype = ContentType.objects.get_for_model(MoneyContribution).pk
    contributions = []
    money_contributions = []

    contribution_fields = [
        'status',
        'contributor_id',
        'created',
        'polymorphic_ctype_id'
    ]
    money_contribution_fields = [
        'contribution_ptr_id',
        'value',
        'value_currency'
    ]

    for donor in Donor.objects.values(
            'id',
            'status',
            'created',
            'amount',
            'amount_currency',
            'contributor_ptr_id',
            'contributor_date'):
        if donor['status'] in ('pending', 'new'):
            status = 'new'
        elif donor['status'] in ('failed', 'refunded', 'activity_refunded', 'cancelled'):
            status = 'failed'
        else:
            status = donor['status']
        contributions.append({
            'polymorphic_ctype_id': money_contribution_ctype,
            'status': status,
            'contributor_id': donor['id'],
            'created': donor['created']
        })
        money_contributions.append({
            'value': donor['amount'],
            'value_currency': donor['amount_currency'],
            'contributor_id': donor['id'],
        })

    insert('activities_contribution', contribution_fields, contributions)

    contributions = dict(Contribution.objects.values_list('contributor_id', 'id'))
    for money_contribution in money_contributions:
        money_contribution['contribution_ptr_id'] = contributions[money_contribution['contributor_id']]

    insert('funding_moneycontribution', money_contribution_fields, money_contributions)


class Migration(migrations.Migration):

    dependencies = [
        ('funding', '0060_auto_20201127_0922'),
    ]

    operations = [
        migrations.RunPython(create_money_contributions, migrations.RunPython.noop),
    ]
