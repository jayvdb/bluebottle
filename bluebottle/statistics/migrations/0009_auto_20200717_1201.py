# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-07-17 10:01


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0008_auto_20200717_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='databasestatistic',
            name='query',
            field=models.CharField(choices=[(b'manual', 'Manual input'), (b'people_involved', 'People involved'), (b'participants', 'Participants'), (b'activities_succeeded', 'Activities succeeded'), (b'assignments_succeeded', 'Tasks succeeded'), (b'events_succeeded', 'Events succeeded'), (b'fundings_succeeded', 'Funding activities succeeded'), (b'assignment_members', 'Task applicants'), (b'event_members', 'Event participants'), (b'assignments_online', 'Tasks online'), (b'events_online', 'Events online'), (b'fundings_online', 'Funding activities online'), (b'donations', 'Donations'), (b'donated_total', 'Donated total'), (b'pledged_total', 'Pledged total'), (b'amount_matched', 'Amount matched'), (b'activities_online', 'Activities Online'), (b'votes_cast', 'Votes casts'), (b'time_spent', 'Time spent'), (b'members', 'Number of members')], db_index=True, max_length=30, verbose_name='query'),
        ),
    ]
