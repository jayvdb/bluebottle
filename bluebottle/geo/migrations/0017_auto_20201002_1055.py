# Generated by Django 3.0.8 on 2020-10-02 08:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import re
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0016_location_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='alpha2_code',
            field=models.CharField(blank=True, help_text='ISO 3166-1 alpha-2 code', max_length=2, validators=[django.core.validators.RegexValidator(re.compile('[A-Z][A-Z]'), 'Enter 2 capital letters.')], verbose_name='alpha2 code'),
        ),
        migrations.AlterField(
            model_name='country',
            name='alpha3_code',
            field=models.CharField(blank=True, help_text='ISO 3166-1 alpha-3 code', max_length=3, validators=[django.core.validators.RegexValidator(re.compile('[A-Z][A-Z][A-Z]'), 'Enter 3 capital letters.')], verbose_name='alpha3 code'),
        ),
        migrations.AlterField(
            model_name='country',
            name='numeric_code',
            field=models.CharField(blank=True, help_text='ISO 3166-1 or M.49 numeric code', max_length=3, null=True, unique=True, validators=[django.core.validators.RegexValidator(re.compile('[0-9][0-9][0-9]'), 'Enter 3 numeric characters.')], verbose_name='numeric code'),
        ),
        migrations.AlterField(
            model_name='countrytranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='geo.Country'),
        ),
        migrations.AlterField(
            model_name='location',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, help_text='Location picture', max_length=255, null=True, upload_to='location_images/', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='region',
            name='numeric_code',
            field=models.CharField(blank=True, help_text='ISO 3166-1 or M.49 numeric code', max_length=3, null=True, unique=True, validators=[django.core.validators.RegexValidator(re.compile('[0-9][0-9][0-9]'), 'Enter 3 numeric characters.')], verbose_name='numeric code'),
        ),
        migrations.AlterField(
            model_name='regiontranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='geo.Region'),
        ),
        migrations.AlterField(
            model_name='subregion',
            name='numeric_code',
            field=models.CharField(blank=True, help_text='ISO 3166-1 or M.49 numeric code', max_length=3, null=True, unique=True, validators=[django.core.validators.RegexValidator(re.compile('[0-9][0-9][0-9]'), 'Enter 3 numeric characters.')], verbose_name='numeric code'),
        ),
        migrations.AlterField(
            model_name='subregiontranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='geo.SubRegion'),
        ),
    ]