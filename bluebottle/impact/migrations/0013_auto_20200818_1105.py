# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-08-18 07:56
from __future__ import unicode_literals

from django.db import migrations, models
from bluebottle.clients import properties
from parler.models import TranslatableModelMixin


def create_default_impact_types(apps, schema_editor):
    ImpactType = apps.get_model('impact', 'ImpactType')
    ImpactType.__bases__ = (models.Model, TranslatableModelMixin)

    ImpactTypeTranslation = apps.get_model('impact', 'ImpactTypeTranslation')
    Language = apps.get_model('utils', 'language')

    languages = [lang.code for lang in Language.objects.all()]

    definitions = [
        {
            'slug': 'co2',
            'icon': 'co2',
            'en': {
                'text': u'Reduce CO₂ emissions',
                'unit': u'kg',
                'text_passed': 'CO₂ emissions reduced',
                'text_with_target': u'Reduce CO₂ emissions by {} kg',
            },
            'nl': {
                'text': u'CO₂ uitstoot verminderen',
                'unit': u'kg',
                'text_passed': 'CO₂ uitstoot met {} kg te verminderen',
                'text_with_target': u'CO₂ uitstoot verminderd'
            }
        },
        {
            'slug': 'people',
            'icon': 'people',
            'en': {
                'text': u'Reach people',
                'unit': u'',
                'text_passed': 'Reach {} people',
                'text_with_target': u'People reached',
            },
            'nl': {
                'text': u'Mensen bereiken',
                'unit': u'',
                'text_passed': '{} mensen te bereiken',
                'text_with_target': u'Mensen bereikt'
            }
        },
        {
            'slug': 'food',
            'icon': '',
            'en': {
                'text': u'Reduce food waste',
                'unit': u'kg',
                'text_passed': 'Reduce food waste by {} kg',
                'text_with_target': u'Food waste reduced',
            },
            'nl': {
                'text': u'Voedselverspilling verminderen',
                'unit': u'kg',
                'text_passed': 'Voedselverspilling met {} kg te verminderen',
                'text_with_target': u'Voedselverspilling verminderd'
            }
        },
        {
            'slug': 'water',
            'icon': 'water',
            'en': {
                'text': u'Save water',
                'unit': u'l',
                'text_passed': 'Save {} l water',
                'text_with_target': u'Water saved',
            },
            'nl': {
                'text': u'Water besparen',
                'unit': u'l',
                'text_passed': '{} l water te besparen',
                'text_with_target': u'Water bespaard'
            }
        },
        {
            'slug': 'plastic',
            'icon': 'plastic',
            'en': {
                'text': u'Save plastic',
                'unit': u'kg',
                'text_passed': 'Save {} kg plastic',
                'text_with_target': u'Plastic saved',
            },
            'nl': {
                'text': u'Plastic besparen',
                'unit': u'kg',
                'text_passed': '{} kg plastic te besparen',
                'text_with_target': u'Plastic bespaard'
            }
        },
        {
            'slug': 'trees',
            'icon': 'trees',
            'en': {
                'text': u'Plant trees',
                'unit': u'',
                'text_passed': 'Plant {} trees',
                'text_with_target': u'Trees planted',
            },
            'nl': {
                'text': u'Bomen planten',
                'unit': u'',
                'text_passed': '{} bomen te planten',
                'text_with_target': u'Bomen geplant'
            }
        },
        {
            'slug': 'jobs',
            'icon': 'jobs',
            'en': {
                'text': u'Create jobs',
                'unit': u'',
                'text_passed': 'Create {} jobs',
                'text_with_target': u'Jobs created',
            },
            'nl': {
                'text': u'Banen creëren',
                'unit': u'',
                'text_passed': '{} banen te creëren',
                'text_with_target': u'Banen gecreëerd'
            }
        },
    ]

    for definition in definitions:
        impact_type, created = ImpactType.objects.get_or_create(
            slug=definition['slug'],
            defaults={
                'active': False,
                'icon': definition['icon']
            }
        )
        if created:
            for language in languages:
                if language in definition:
                    ImpactTypeTranslation.objects.get_or_create(
                        language_code=language,
                        master=impact_type,
                        defaults=definition[language]
                    )


class Migration(migrations.Migration):

    dependencies = [
        ('impact', '0012_auto_20200817_1608'),
    ]

    operations = [
        migrations.RunPython(create_default_impact_types)
    ]