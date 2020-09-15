# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-31 11:27


import bluebottle.utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_categorycontent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorycontent',
            options={'ordering': ['sequence'], 'verbose_name': 'content block', 'verbose_name_plural': 'content blocks'},
        ),
        migrations.AddField(
            model_name='categorycontent',
            name='sequence',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='categorycontent',
            name='description',
            field=models.TextField(blank=True, default=b'', help_text='Max: 190 characters.', max_length=190, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='categorycontent',
            name='image',
            field=bluebottle.utils.fields.ImageField(blank=True, help_text='Accepted file format: .jpg, .jpeg & .png', max_length=255, null=True, upload_to=b'categories/content/', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='categorycontent',
            name='link_text',
            field=models.CharField(blank=True, default='Read more', help_text='The link will only be displayed if an URL is provided. Max: 60 characters.', max_length=60, verbose_name='link name'),
        ),
        migrations.AlterField(
            model_name='categorycontent',
            name='title',
            field=models.CharField(help_text='Max: 60 characters.', max_length=60, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='categorycontent',
            name='video_url',
            field=models.URLField(blank=True, default=b'', help_text='Setting a video url will replace the image. Only YouTube or Vimeo videos are accepted. Max: 100 characters.', max_length=100),
        ),
    ]
