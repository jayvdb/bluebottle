# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-03 14:24
from __future__ import unicode_literals

import bluebottle.files.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0007_auto_20201021_1315'),
        ('time_based', '0023_auto_20201103_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='onadateapplication',
            name='document',
            field=bluebottle.files.fields.PrivateDocumentField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='files.PrivateDocument'),
        ),
        migrations.AddField(
            model_name='onadateapplication',
            name='motivation',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='periodapplication',
            name='document',
            field=bluebottle.files.fields.PrivateDocumentField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='files.PrivateDocument'),
        ),
        migrations.AddField(
            model_name='periodapplication',
            name='motivation',
            field=models.TextField(blank=True),
        ),
    ]