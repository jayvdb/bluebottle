# Generated by Django 3.0.8 on 2020-10-02 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('segments', '0005_auto_20201002_1055'),
        ('activities', '0025_merge_20200819_1654'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organizer',
            options={'verbose_name': 'Activity owner', 'verbose_name_plural': 'Activity owners'},
        ),
        migrations.AlterField(
            model_name='activity',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='review_status',
            field=models.CharField(default='draft', max_length=40),
        ),
        migrations.AlterField(
            model_name='activity',
            name='segments',
            field=models.ManyToManyField(blank=True, related_name='activities', to='segments.Segment', verbose_name='Segment'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='slug',
            field=models.SlugField(default='new', max_length=100, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='status',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='activity',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='video_url',
            field=models.URLField(blank=True, default='', help_text="Do you have a video pitch or a short movie that explains your activity? Cool! We can't wait to see it! You can paste the link to YouTube or Vimeo video here", max_length=100, null=True, verbose_name='video'),
        ),
    ]
