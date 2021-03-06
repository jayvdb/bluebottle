# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-22 14:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('payments', '0003_auto_20161025_1221'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelesomPayment',
            fields=[
                ('payment_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payments.Payment')),
                ('amount', models.CharField(blank=True, help_text=b'Amount', max_length=200, null=True)),
                ('currency', models.CharField(blank=True, default=b'USD', help_text=b'Transaction currency', max_length=200, null=True)),
                ('mobile', models.CharField(blank=True, help_text=b'Mobile Number', max_length=200, null=True)),
                ('transaction_reference', models.CharField(blank=True, help_text=b'Transaction reference for tracking transaction', max_length=100, null=True)),
                ('description', models.CharField(blank=True, help_text=b'Description', max_length=200, null=True)),
                ('response', models.TextField(blank=True, help_text='Response from Telesom', null=True)),
                ('update_response', models.TextField(blank=True, help_text='Result from Telesom (status update)', null=True)),
            ],
            options={
                'ordering': ('-created', '-updated'),
                'verbose_name': 'Telesom/Zaad Payment',
                'verbose_name_plural': 'Telesom/Zaad Payments',
            },
            bases=('payments.payment',),
        ),
    ]
