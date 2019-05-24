# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-05-22 11:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_add_permissions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={'permissions': (('api_read_participant', 'Can view participant through the API'), ('api_add_participant', 'Can add participant through the API'), ('api_change_participant', 'Can change participant through the API'), ('api_delete_participant', 'Can delete participant through the API'), ('api_read_own_participant', 'Can view own participant through the API'), ('api_add_own_participant', 'Can add own participant through the API'), ('api_change_own_participant', 'Can change own participant through the API'), ('api_delete_own_participant', 'Can delete own participant through the API')), 'verbose_name': 'Participant', 'verbose_name_plural': 'Participants'},
        ),
    ]
