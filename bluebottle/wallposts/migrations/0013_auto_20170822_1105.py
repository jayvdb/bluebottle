# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-22 09:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallposts', '0012_auto_20170821_2018'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mediawallpost',
            options={'permissions': (('api_read_own_textwallpost', 'Can view own text wallposts through the API'), ('api_change_own_textwallpost', 'Can change text wallposts through the API'), ('api_delete_own_textwallpost', 'Can delete own text wallposts through the API'), ('api_read_textwallpost', 'Can view text wallposts through the API'), ('api_add_textwallpost', 'Can add text wallposts through the API'), ('api_change_textwallpost', 'Can change text wallposts through the API'), ('api_delete_textwallpost', 'Can delete text wallposts through the API'), ('api_read_mediawallpost', 'Can view media wallposts through the API'), ('api_add_mediawallpost', 'Can add media wallposts through the API'), ('api_change_mediawallpost', 'Can change media wallposts through the API'), ('api_delete_mediawallpost', 'Can delete media wallposts through the API'), ('api_read_own_mediawallpost', 'Can view own media wallposts through the API'), ('api_change_own_mediawallpost', 'Can change own media wallposts through the API'), ('api_delete_own_mediawallpost', 'Can delete own media wallposts through the API'), ('api_read_mediawallpostphoto', 'Can view media wallpost photos through the API'), ('api_add_mediawallpostphoto', 'Can add media wallpost photos through the API'), ('api_change_mediawallpostphoto', 'Can change media wallpost photos through the API'), ('api_delete_mediawallpostphoto', 'Can delete media wallpost photos through the API'), ('api_read_own_mediawallpostphoto', 'Can view own media wallpost photos through the API'), ('api_change_own_mediawallpostphoto', 'Can change own media wallpost photos through the API'), ('api_delete_own_mediawallpostphoto', 'Can delete own media wallpost photos through the API'))},
        ),
        migrations.AlterModelOptions(
            name='reaction',
            options={'base_manager_name': 'objects_with_deleted', 'ordering': ('created',), 'permissions': (('api_read_reaction', 'Can view reactions through the API'), ('api_add_reaction', 'Can add reactions through the API'), ('api_change_reaction', 'Can reactions documents through the API'), ('api_delete_reaction', 'Can reactions documents through the API'), ('api_read_own_reaction', 'Can view own reactions through the API'), ('api_add_own_reaction', 'Can add own reactions through the API'), ('api_change_own_reaction', 'Can change own reactions documents through the API'), ('api_delete_own_reaction', 'Can delete own reactions documents through the API')), 'verbose_name': 'Reaction', 'verbose_name_plural': 'Reactions'},
        ),
        migrations.AlterModelOptions(
            name='wallpost',
            options={'base_manager_name': 'objects_with_deleted', 'ordering': ('created',), 'permissions': (('api_read_wallpost', 'Can view wallposts through the API'), ('api_add_wallpost', 'Can add wallposts through the API'), ('api_change_wallpost', 'Can wallposts documents through the API'), ('api_delete_wallpost', 'Can wallposts documents through the API'), ('api_read_own_wallpost', 'Can view own wallposts through the API'), ('api_change_own_wallpost', 'Can own wallposts documents through the API'), ('api_delete_own_wallpost', 'Can own wallposts documents through the API'))},
        ),
    ]
