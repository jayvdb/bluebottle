# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 15:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


def forwards_func(apps, schema_editor):
        Stat = apps.get_model('cms', 'Stat')
        StatTranslation = apps.get_model('cms', 'StatTranslation')

        for object in Stat.objects.all():
            StatTranslation.objects.create(
                master_id=object.pk,
                language_code=settings.LANGUAGE_CODE,
                title=object.title
            )


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_auto_20161207_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=63)),
            ],
            options={
                'managed': True,
                'db_table': 'cms_stat_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'stat Translation',
            },
        ),
        migrations.AddField(
            model_name='stattranslation',
            name='master',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='cms.Stat'),
        ),
        migrations.RunPython(forwards_func),
        migrations.RemoveField(
            model_name='stat',
            name='title',
        ),
        migrations.AlterUniqueTogether(
            name='stattranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
