# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-05 12:26


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payouts', '0005_auto_20160721_1114'),
    ]

    operations = [
        migrations.AlterField(model_name='ProjectPayout',
                              name='receiver_account_bic',
                              field=models.CharField(max_length=255, blank=True)),
        migrations.RenameField(model_name='ProjectPayout',
                               old_name='receiver_account_bic',
                               new_name='receiver_account_details')
    ]
