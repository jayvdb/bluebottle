# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-11-06 08:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('initiatives', '0017_auto_20191031_1439'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='initiativeplatformsettings',
            options={'verbose_name': 'initiative settings', 'verbose_name_plural': 'initiative settings'},
        ),
        migrations.AddField(
            model_name='initiativeplatformsettings',
            name='contact_method',
            field=models.CharField(choices=[(b'mail', 'E-mail'), (b'phone', 'Phone')], default=b'mail', max_length=100),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='geo.Location', verbose_name='Office location'),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='geo.Geolocation', verbose_name='Impact location'),
        ),
        migrations.AlterField(
            model_name='initiative',
            name='promoter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='promoter_initiatives', to=settings.AUTH_USER_MODEL, verbose_name='promoter'),
        ),
        migrations.AlterField(
            model_name='initiativeplatformsettings',
            name='activity_types',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(b'funding', 'Funding'), (b'event', 'Events'), (b'assignment', 'Assignment')], max_length=100),
        ),
        migrations.AlterField(
            model_name='initiativeplatformsettings',
            name='search_filters',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(b'location', 'Location'), (b'date', 'Date'), (b'skill', 'Skill'), (b'type', 'Type'), (b'theme', 'Theme'), (b'category', 'Category'), (b'status', 'Status')], max_length=1000),
        ),
    ]