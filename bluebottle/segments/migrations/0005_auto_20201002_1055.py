# Generated by Django 3.0.8 on 2020-10-02 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('segments', '0004_auto_20200708_1404'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='segment',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='segmenttype',
            options={'ordering': ('name',)},
        ),
    ]