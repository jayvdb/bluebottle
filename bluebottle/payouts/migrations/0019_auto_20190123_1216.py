# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2019-01-23 11:16


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payouts', '0018_auto_20190108_0858'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripepayoutaccount',
            name='document_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        )
    ]
