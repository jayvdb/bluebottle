# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-07-17 08:21
from __future__ import unicode_literals

import bluebottle.utils.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0066_auto_20180709_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteplatformsettings',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to=b'site_content/', validators=[bluebottle.utils.validators.FileExtensionValidator([b'svg'], None, b'invalid_extension')]),
        ),
    ]
