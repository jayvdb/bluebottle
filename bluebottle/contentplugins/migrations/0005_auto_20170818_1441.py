# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-18 12:41


from django.db import migrations

from bluebottle.utils.utils import update_group_permissions


def add_group_permissions(apps, schema_editor):
    group_perms = {
        'Staff': {
            'perms': (
                'add_contenttype', 'change_contenttype', 'delete_contenttype',
            )
        }
    }
    update_group_permissions('contenttypes', group_perms, apps)

    group_perms = {
        'Staff': {
            'perms': (
                'add_oembeditem', 'change_oembeditem', 'delete_oembeditem',
            )
        }
    }
    update_group_permissions('oembeditem', group_perms, apps)


    group_perms = {
        'Staff': {
            'perms': (
                'add_rawhtmlitem', 'change_rawhtmlitem', 'delete_rawhtmlitem',
            )
        }
    }
    update_group_permissions('rawhtml', group_perms, apps)

    group_perms = {
        'Staff': {
            'perms': (
                'add_textitem', 'change_textitem', 'delete_textitem',
            )
        }
    }
    update_group_permissions('text', group_perms, apps)

    group_perms = {
        'Staff': {
            'perms': (
                'add_placeholder', 'change_placeholder', 'delete_placeholder',
                'add_contentitem', 'change_contentitem', 'delete_contentitem',
            )
        }
    }
    update_group_permissions('fluent_contents', group_perms, apps)


    group_perms = {
        'Staff': {
            'perms': (
                'add_pictureitem', 'change_pictureitem', 'delete_pictureitem',
            )
        }
    }
    update_group_permissions('contentplugins', group_perms, apps)


class Migration(migrations.Migration):

    dependencies = [
            # FIX: add other dependencies
        ('contentplugins', '0004_merge_20170124_1338'),
        ('contenttypes', '0001_initial'),
        ('oembeditem', '0001_initial'),
        ('rawhtml', '0001_initial'),
        ('text', '0001_initial'),
        ('fluent_contents', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_group_permissions)
    ]
