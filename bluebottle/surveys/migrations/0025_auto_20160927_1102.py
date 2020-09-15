# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-27 09:02


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0024_auto_20160926_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='user_type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='aggregateanswer',
            name='aggregation_type',
            field=models.CharField(choices=[(b'project', b'Project'), (b'initiator', b'Project initiator'), (b'organization', b'Partner organisation'), (b'task', b'Task'), (b'project_tasks', b'Tasks in project'), (b'combined', b'Project and tasks')], default=b'project', max_length=20),
        ),
    ]
