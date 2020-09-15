# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-24 08:10


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0023_auto_20171019_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='SitePlatformSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update', models.DateTimeField(auto_now=True)),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contact_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('copyright', models.CharField(blank=True, max_length=100, null=True)),
                ('powered_by_text', models.CharField(blank=True, max_length=100, null=True)),
                ('powered_by_link', models.CharField(blank=True, max_length=100, null=True)),
                ('powered_by_logo', models.ImageField(blank=True, null=True, upload_to=b'site_content/')),
            ],
            options={
                'verbose_name': 'site platform settings',
                'verbose_name_plural': 'site platform settings',
            },
        ),
    ]
