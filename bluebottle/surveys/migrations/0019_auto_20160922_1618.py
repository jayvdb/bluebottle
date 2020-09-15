# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-22 14:18


from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields.json


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0018_auto_20160922_1610'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remote_id', models.CharField(blank=True, max_length=200, null=True)),
                ('type', models.CharField(blank=True, max_length=200, null=True)),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('specification', django_extensions.db.fields.json.JSONField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='question',
            name='sub_questions',
        ),
        migrations.AddField(
            model_name='subquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Question'),
        ),
    ]
