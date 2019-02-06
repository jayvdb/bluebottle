# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-06-06 10:25
from __future__ import unicode_literals

from django.db import migrations
from django.core.management import call_command


def generate_looker_embeds(apps, schema_editor):

    ProjectPlatformSettings = apps.get_model('projects', 'ProjectPlatformSettings')
    project_settings, created = ProjectPlatformSettings.objects.get_or_create()

    LookerEmbed = apps.get_model('looker', 'LookerEmbed')
    LookerEmbed.objects.all().delete()

    call_command('loaddata', 'looker_projects')

    if 'sourcing' in project_settings.create_types:
        call_command('loaddata', 'looker_activities')

    if 'funding' in project_settings.create_types:
        call_command('loaddata', 'looker_giving')


def dummy(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('looker', '0002_auto_20180328_1054'),
        ('projects', '0054_auto_20171122_1415'),
        ('social_django', '0002_add_related_name'),  # No idea why, but this fixes a nasty error about pending trigger events during the migrations
    ]

    operations = [
        migrations.RunPython(generate_looker_embeds, dummy)

    ]
