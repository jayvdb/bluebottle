# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-23 13:25
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields
from django.db.models.fields import DecimalField


class MoneyField(DecimalField):
    """
    Deprecated MoneyField
    """
    def __init__(self, *args, **kwargs):
        """ Set defaults to 2 decimal places and 12 digits. """
        kwargs['max_digits'] = kwargs.get('max_digits', 12)
        kwargs['decimal_places'] = kwargs.get('decimal_places', 2)
        super(MoneyField, self).__init__(*args, **kwargs)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DonationJournal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', MoneyField(decimal_places=2, max_digits=12, verbose_name='amount')),
                ('user_reference', models.CharField(blank=True, max_length=100, verbose_name=b'user reference')),
                ('description', models.CharField(blank=True, max_length=400)),
                ('date', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderPaymentJournal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', MoneyField(decimal_places=2, max_digits=12, verbose_name='amount')),
                ('user_reference', models.CharField(blank=True, editable=False, max_length=100, verbose_name=b'user reference')),
                ('description', models.CharField(blank=True, max_length=400)),
                ('date', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationPayoutJournal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', MoneyField(decimal_places=2, max_digits=12, verbose_name='amount')),
                ('user_reference', models.CharField(blank=True, max_length=100, verbose_name=b'user reference')),
                ('description', models.CharField(blank=True, max_length=400)),
                ('date', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectPayoutJournal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', MoneyField(decimal_places=2, max_digits=12, verbose_name='amount')),
                ('user_reference', models.CharField(blank=True, max_length=100, verbose_name=b'user reference')),
                ('description', models.CharField(blank=True, max_length=400)),
                ('date', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
