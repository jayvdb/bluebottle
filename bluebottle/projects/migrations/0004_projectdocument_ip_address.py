# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-14 11:54


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20160610_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectdocument',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, default=None, null=True, verbose_name='IP address'),
        ),
    ]
