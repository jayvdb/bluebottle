# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-24 09:24
from __future__ import unicode_literals

import bluebottle.utils.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0022_task_accepting'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmember',
            name='resume',
            field=bluebottle.utils.fields.PrivateFileField(blank=True, upload_to=b'private/private/private/task-members/resume'),
        ),
    ]
