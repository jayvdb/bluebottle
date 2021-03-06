# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-14 09:35
from __future__ import unicode_literals

import bluebottle.utils.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0009_organization_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name'], 'verbose_name': 'partner organization', 'verbose_name_plural': 'partner organizations'},
        ),
        migrations.AlterField(
            model_name='organization',
            name='logo',
            field=bluebottle.utils.fields.ImageField(blank=True, help_text='Partner Organization Logo', max_length=255, null=True, upload_to=b'partner_organization_logos/', verbose_name='logo'),
        ),
    ]
