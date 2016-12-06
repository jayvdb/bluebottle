# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-06 10:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('fluent_contents', '0001_initial'),
        ('projects', '0015_auto_20161206_1043'),
        ('cms', '0007_auto_20161205_2018'),
    ]

    operations = [
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projects', models.ManyToManyField(to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectsContent',
            fields=[
                ('contentitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('title', models.CharField(blank=True, max_length=63, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=100, null=True)),
                ('action', models.CharField(max_length=255)),
                ('action_text', models.CharField(max_length=255)),
                ('projects', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Projects')),
            ],
            options={
                'db_table': 'contentitem_cms_projectscontent',
                'verbose_name': 'Projects',
            },
            bases=('fluent_contents.contentitem',),
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('base_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RenameModel(
            old_name='ResultsContent',
            new_name='SurveyContent',
        ),
        migrations.AlterModelTable(
            name='surveycontent',
            table='contentitem_cms_surveycontent',
        ),
    ]
