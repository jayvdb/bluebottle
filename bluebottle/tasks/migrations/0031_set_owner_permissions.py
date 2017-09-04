# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-22 09:27
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import Permission, Group

from bluebottle.utils.utils import update_group_permissions


def set_owner_permissions(apps, schema_editor):
    group_perms = {
        'Staff': {
            'perms': ('api_read_taskmember_resume', )
        },
        'Anonymous': {
            'perms': ('api_read_task', 'api_read_skill')
        },
        'Authenticated': {
            'perms': (
                'api_read_task', 'api_add_own_task', 'api_change_own_task',
                'api_read_taskmember', 'api_add_own_taskmember',
                'api_change_own_taskmember', 'api_delete_own_taskmember',
                'api_read_own_taskmember_resume',
                'api_read_skill'
            )
        }
    }
    update_group_permissions('tasks', group_perms, apps)

    authenticated = Group.objects.get(name='Authenticated')
    for perm in (
        'api_add_task', 'api_change_task', 'api_delete_task',
        'api_add_taskmember', 'api_change_taskmember', 'api_delete_taskmember'
        ):
        authenticated.permissions.remove(
            Permission.objects.get(
                codename=perm, content_type__app_label='tasks'
            )
        )

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0030_auto_20170822_1104'),
    ]

    operations = [
        migrations.RunPython(set_owner_permissions)
    ]
