# Generated by Django 3.0.8 on 2020-10-02 08:55

import bluebottle.utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0016_auto_20200106_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='logo',
            field=bluebottle.utils.fields.ImageField(blank=True, help_text='Partner Organization Logo', max_length=255, null=True, upload_to='partner_organization_logos/', verbose_name='logo'),
        ),
    ]