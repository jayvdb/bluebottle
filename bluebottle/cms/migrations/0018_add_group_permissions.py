# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-03 14:14


from django.db import migrations

from bluebottle.utils.utils import update_group_permissions


def add_group_permissions(apps, schema_editor):
    group_perms = {
        'Staff': {
            'perms': (
                'add_resultpage', 'change_resultpage', 'delete_resultpage',
                'add_stats', 'change_stats', 'delete_stats',
                'add_statscontent', 'change_statscontent', 'delete_statscontent',
                'add_stat', 'change_stat', 'delete_stat',
                'add_quotes', 'change_quotes', 'delete_quotes',
                'add_quote', 'change_quote', 'delete_quote',
                'add_quotescontent', 'change_quotescontent', 'delete_quotescontent',
                'add_projects', 'change_projects', 'delete_projects',
                'add_projectscontent', 'change_projectscontent', 'delete_projectscontent',
                'add_shareresultscontent', 'change_shareresultscontent', 'delete_shareresultscontent',
                'add_projectimagescontent', 'change_projectimagescontent', 'delete_projectimagescontent',
                'add_projectsmapcontent', 'change_projectsmapcontent', 'delete_projectsmapcontent',
                'add_supportertotalcontent', 'change_supportertotalcontent', 'delete_supportertotalcontent',
            )
        }
    }

    update_group_permissions('cms', group_perms, apps)


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0017_add_api_permissions'),
    ]

    operations = [
            migrations.RunPython(add_group_permissions)
    ]
