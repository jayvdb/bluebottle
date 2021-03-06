# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-27 12:19
from __future__ import unicode_literals

from django.db import migrations, connection
from django.core.management import call_command


def migrate_homepage(apps, schema_editor):
    call_command('migrate_homepage', tenant=connection.tenant.schema_name)


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0051_auto_20171024_1631'),
    ]

    operations = [
        migrations.RunPython(migrate_homepage)
    ]
