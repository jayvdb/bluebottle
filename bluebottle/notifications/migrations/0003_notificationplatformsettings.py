# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-11-06 08:28


from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_message_custom_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationPlatformSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update', models.DateTimeField(auto_now=True)),
                ('share_options', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(b'twitter', 'Twitter'), (b'facebook', 'Facebook'), (b'facebookAtWork', 'Facebook at Work'), (b'linkedin', 'LinkedIn'), (b'whatsapp', 'Whatsapp'), (b'email', 'Email')], max_length=100)),
                ('facebook_at_work_url', models.URLField(blank=True, max_length=100, null=True)),
                ('match_options', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(b'theme', 'Theme'), (b'skill', 'Skill'), (b'location', 'Location')], max_length=100)),
            ],
            options={
                'verbose_name': 'notification/matching settings',
                'verbose_name_plural': 'notification/matching settings',
            },
        ),
    ]
