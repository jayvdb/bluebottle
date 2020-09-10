# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-09-03 09:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('slides', '0006_auto_20180717_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='slide',
            name='video',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to=b'banner_slides/', verbose_name='Background video'),
        ),
        migrations.AlterField(
            model_name='slide',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='slide',
            name='language',
            field=models.CharField(choices=[(b'nl', b'Dutch'), (b'en', b'English')], max_length=5, verbose_name='language'),
        ),
        migrations.AlterField(
            model_name='slide',
            name='publication_date',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, help_text="To go live, status must be 'Published'.", null=True, verbose_name='publication date'),
        ),
    ]
