# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-18 08:50


from django.db import migrations


def set_reviewed(apps, schema_editor):
    Project = apps.get_model('projects', 'Project')

    for project in Project.objects.filter(
        status__slug__in=(
        'closed', 'voting-done', 'done-complete', 'refunded', 'done-incomplete'
        )
    ):
        project.bank_details_reviewed = True
        project.save()

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0076_auto_20180516_0954'),
    ]

    operations = [
        migrations.RunPython(set_reviewed)
    ]
