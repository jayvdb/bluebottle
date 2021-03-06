# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-02-25 11:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0029_merge_20190222_0930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='place',
        ),
        migrations.AddField(
            model_name='member',
            name='matching_options_set',
            field=models.DateTimeField(null=True, blank=True, help_text='When the user updated their matching preferences.'),
        ),
        migrations.AlterField(
            model_name='member',
            name='location',
            field=models.ForeignKey(blank=True, help_text='Location', null=True, on_delete=django.db.models.deletion.SET_NULL, to='geo.Location'),
        ),
        migrations.AlterField(
            model_name='member',
            name='verified',
            field=models.BooleanField(default=False, help_text='Was verified for voting by recaptcha.'),
        ),
    ]
