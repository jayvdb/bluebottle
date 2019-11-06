# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-07-10 07:38
from __future__ import unicode_literals

import bluebottle.utils.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('fluent_contents', '0001_initial'),
        ('cms', '0066_auto_20180709_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivitiesContent',
            fields=[
                ('contentitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=400, null=True)),
                ('action_text', models.CharField(blank=True, default='Find more activities', max_length=80, null=True)),
                ('action_link', models.CharField(blank=True, default=b'/initiatives/activities/list', max_length=100, null=True)),
                ('highlighted', models.BooleanField(default=False)),
                ('activities', models.ManyToManyField(blank=True, db_table=b'cms_activitycontent_activities', to='activities.Activity')),
            ],
            options={
                'db_table': 'contentitem_cms_activitiescontent',
                'verbose_name': 'Activities',
            },
            bases=('fluent_contents.contentitem',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        )
    ]