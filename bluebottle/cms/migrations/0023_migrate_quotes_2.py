# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-10-06 08:15


from django.db import migrations, models
import django.db.models.deletion


def migrate_quotes(apps, schema_editor):
    Quote = apps.get_model('cms', 'Quote')
    for quote in Quote.objects.all():
        pk = quote.pk
        # There might be multiple pages using the same list
        # so we iterate and make copies and then delete the original
        translations = quote.translations.all()
        for block in quote.quotes.quote_list.all():
            new_quote = quote
            new_quote.block = block
            new_quote.pk = None
            new_quote.save()
            new_quote.translations = translations
            new_quote.save()
        Quote.objects.filter(pk=pk).all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_migrate_quotes_1'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='QuotesContent',
            managers=[
                ('objects', models.manager.Manager()),
            ],
        ),
        migrations.RunPython(migrate_quotes),
    ]
