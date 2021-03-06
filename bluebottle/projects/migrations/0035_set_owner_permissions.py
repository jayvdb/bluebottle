# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-22 09:09
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import Permission, Group

from bluebottle.utils.utils import update_group_permissions



def set_owner_permissions(apps, schema_editor):
    group_perms = {
        'Staff': {
            'perms': (
                'api_read_projectdocument',
            )
        },
        'Authenticated': {
            'perms': (
                'api_change_own_project', 'api_add_own_project',
                'api_read_own_project',
                'api_add_own_projectdocument', 'api_read_own_projectdocument',
                'api_change_own_projectdocument',
                'api_add_own_projectbudgetline', 'api_read_own_projectbudgetline',
                'api_change_own_projectbudgetline', 'api_delete_own_projectbudgetline',
            )
        }
    }

    update_group_permissions('projects', group_perms, apps)

    authenticated = Group.objects.get(name='Authenticated')
    for perm in (
        'api_change_project', 'api_delete_project', 'api_change_projectbudgetline',
        'api_read_projectdocument', 'api_change_projectdocument', 'api_delete_projectbudgetline',
        ):
        authenticated.permissions.remove(
            Permission.objects.get(
                codename=perm, content_type__app_label='projects'
            )
        )


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0034_auto_20170822_1303'),
    ]

    operations = [
        migrations.RunPython(set_owner_permissions)
    ]
