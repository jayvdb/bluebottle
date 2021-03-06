# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-25 10:53
from __future__ import unicode_literals

import bluebottle.utils.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('projects', '0042_merge_20170920_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectAddOn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_projects.projectaddon_set+', to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='projectaddon',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addons', to='projects.Project'),
        ),
    ]
