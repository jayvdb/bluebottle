# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-30 13:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0006_migrate_geo_translations'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'verbose_name': 'country', 'verbose_name_plural': 'countries'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'verbose_name': 'region', 'verbose_name_plural': 'regions'},
        ),
        migrations.AlterModelOptions(
            name='subregion',
            options={'verbose_name': 'sub region', 'verbose_name_plural': 'sub regions'},
        ),
        migrations.RenameField(
            model_name='countrytranslation',
            old_name='_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='regiontranslation',
            old_name='_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='subregiontranslation',
            old_name='_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='country',
            name='name',
        ),
        migrations.RemoveField(
            model_name='region',
            name='name',
        ),
        migrations.RemoveField(
            model_name='subregion',
            name='name',
        ),
    ]