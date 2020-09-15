# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 08:00


from django.db import migrations
import multiselectfield


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_auto_20161115_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='currencies',
            field=multiselectfield.MultiSelectField(choices=[(b'EUR', 'Euro')], default=[], max_length=100),
        ),
    ]


