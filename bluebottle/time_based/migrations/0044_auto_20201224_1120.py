# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-12-24 10:20
from __future__ import unicode_literals

from django.db import migrations


def fix_wallpost_ctype(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Assignment = apps.get_model('assignments', 'Assignment')
    Event = apps.get_model('events', 'Event')

    Activity = apps.get_model('activities', 'Activity')
    Wallpost = apps.get_model('wallposts', 'Wallpost')

    assigment_ctype = ContentType.objects.get_for_model(Assignment)
    event_ctype = ContentType.objects.get_for_model(Event)
    posts = Wallpost.objects.filter(content_type__in=[event_ctype, assigment_ctype])
    for post in posts:
        act = Activity.objects.get(pk=post.object_id)
        post.content_type = act.polymorphic_ctype
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('time_based', '0043_auto_20201217_0743'),
    ]

    operations = [
        migrations.RunPython(fix_wallpost_ctype, migrations.RunPython.noop)
    ]
