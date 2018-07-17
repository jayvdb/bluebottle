# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-07-17 08:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0004_merge_20170124_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='publication_date',
            field=models.DateTimeField(db_index=True, help_text="To go live, status must be 'Published'.", null=True, verbose_name='publication date'),
        ),
    ]
