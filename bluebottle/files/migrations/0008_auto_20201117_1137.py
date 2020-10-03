# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-17 10:37
from __future__ import unicode_literals

import bluebottle.utils.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0007_auto_20201021_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to='files', validators=[bluebottle.utils.validators.FileMimetypeValidator(['image/png', 'image/jpeg', 'image/gif', 'image/tiff', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/pdf', 'application/vnd.oasis.opendocument.text', 'text/rtf'], None, 'invalid_mimetype'), bluebottle.utils.validators.validate_file_infection], verbose_name='file'),
        ),
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.FileField(upload_to='files', validators=[bluebottle.utils.validators.FileMimetypeValidator(['image/png', 'image/jpeg', 'image/gif', 'image/tiff', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/pdf', 'application/vnd.oasis.opendocument.text', 'text/rtf'], None, 'invalid_mimetype'), bluebottle.utils.validators.validate_file_infection], verbose_name='file'),
        ),
    ]