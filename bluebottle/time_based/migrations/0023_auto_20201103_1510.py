# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-05-24 09:59
from __future__ import unicode_literals

from django.db import migrations, connection

from bluebottle.utils.utils import update_group_permissions

from bluebottle.clients import properties
from bluebottle.clients.models import Client
from bluebottle.clients.utils import LocalTenant


def add_group_permissions(apps, schema_editor):
    tenant = Client.objects.get(schema_name=connection.tenant.schema_name)
    with LocalTenant(tenant):
        group_perms = {
            'Staff': {
                'perms': (
                    'add_onadateapplication', 'change_onadateapplication', 
                    'delete_onadateapplication',

                    'add_periodapplication', 'change_periodapplication', 
                    'delete_periodapplication',
                )
            },
            'Anonymous': {
                'perms': (
                    'api_read_onadateapplication',
                    'api_read_periodapplication',
                ) if not properties.CLOSED_SITE else ()
            },
            'Authenticated': {
                'perms': (
                    'api_read_onadateapplication', 'api_add_onadateapplication', 
                    'api_change_own_onadateapplication', 'api_delete_own_onadateapplication',

                    'api_read_periodapplication', 'api_add_periodapplication', 
                    'api_change_own_periodapplication', 'api_delete_own_periodapplication',
                )
            }
    }

    update_group_permissions('time_based', group_perms, apps)


class Migration(migrations.Migration):

    dependencies = [
        ('time_based', '0022_auto_20201102_1559'),
    ]

    operations = [
        migrations.RunPython(
            add_group_permissions,
            migrations.RunPython.noop
        )
    ]