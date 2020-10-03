# Generated by Django 3.0.8 on 2020-10-02 08:55

import bluebottle.files.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0007_auto_20201002_1055'),
        ('assignments', '0020_auto_20200401_1223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='end_date',
        ),
        migrations.AlterField(
            model_name='applicant',
            name='document',
            field=bluebottle.files.fields.PrivateDocumentField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='files.PrivateDocument'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='motivation',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='end_date_type',
            field=models.CharField(blank=True, choices=[('deadline', 'Deadline'), ('on_date', 'On specific date')], default=None, help_text='Does the task have a deadline or does it take place on a specific date.', max_length=50, null=True, verbose_name='date type'),
        ),
    ]
