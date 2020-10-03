# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-11-08 11:22
from __future__ import unicode_literals

from django.contrib.gis.geos import Point
from django.db import migrations
from django.db.models import Q


def fix_missing_geopositions(apps, schema_editor):
    Initiative = apps.get_model('initiatives', 'Initiative')
    Project = apps.get_model('projects', 'Project')
    for initiative in Initiative.objects.filter(Q(place__position__isnull=True) | Q(place__position=Point(0, 0))):
        project = Project.objects.exclude(projectlocation__isnull=True).filter(slug=initiative.slug).first()
        if initiative.place and project and project.projectlocation \
                and project.projectlocation.latitude\
                and project.projectlocation.longitude:
            initiative.place.position = Point(
                x=float(project.projectlocation.longitude),
                y=float(project.projectlocation.latitude)
            )
            initiative.place.save()


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0017_auto_20191031_1439'),
    ]

    operations = [
        #migrations.RunPython(fix_missing_geopositions, migrations.RunPython.noop)
    ]
