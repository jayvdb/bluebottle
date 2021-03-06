# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-07 09:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terms', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='terms',
            options={'ordering': ('-date',), 'permissions': (('api_read_terms', 'Can view terms through API'),), 'verbose_name': 'Term', 'verbose_name_plural': 'Terms'},
        ),
        migrations.AlterModelOptions(
            name='termsagreement',
            options={'ordering': ('-created',), 'permissions': (('api_read_termsagreement', 'Can view terms agreements through API'),), 'verbose_name': 'Term agreements', 'verbose_name_plural': 'Terms agreement'},
        ),
    ]
