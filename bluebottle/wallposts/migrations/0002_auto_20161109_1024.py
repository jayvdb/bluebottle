# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-09 09:24
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('wallposts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reaction',
            options={'base_manager_name': 'objects_with_deleted', 'ordering': ('created',), 'verbose_name': 'Reaction', 'verbose_name_plural': 'Reactions'},
        ),
        migrations.AlterModelOptions(
            name='wallpost',
            options={'base_manager_name': 'objects_with_deleted', 'ordering': ('created',)},
        ),
        migrations.AlterModelManagers(
            name='mediawallpost',
            managers=[
                ('objects_with_deleted', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='reaction',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('objects_with_deleted', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='systemwallpost',
            managers=[
                ('objects_with_deleted', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='textwallpost',
            managers=[
                ('objects_with_deleted', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='wallpost',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('objects_with_deleted', django.db.models.manager.Manager()),
            ],
        ),
    ]