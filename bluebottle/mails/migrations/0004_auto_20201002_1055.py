# Generated by Django 3.0.8 on 2020-10-02 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0003_auto_20180727_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailplatformsettings',
            name='email_logo',
            field=models.ImageField(blank=True, null=True, upload_to='site_content/'),
        ),
    ]
