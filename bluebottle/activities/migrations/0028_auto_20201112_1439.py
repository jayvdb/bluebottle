# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-11-12 13:39
from __future__ import unicode_literals

from django.db import migrations, models

class RenameModelAndBaseOperation(migrations.RenameModel):

    def __init__(self, old_name, new_name):
        super(RenameModelAndBaseOperation, self).__init__(old_name, new_name)

    def state_forwards(self, app_label, state):
        old_remote_model = '%s.%s' % (app_label, self.old_name_lower)
        new_remote_model = '%s.%s' % (app_label, self.new_name_lower)
        to_reload = []
        # change all bases affected by rename
        for (model_app_label, model_name), model_state in state.models.items():
            if old_remote_model in model_state.bases:
                new_bases_tuple = tuple(
                    new_remote_model if base == old_remote_model
                    else base
                    for base in model_state.bases)
                state.models[model_app_label, model_name].bases = new_bases_tuple
                to_reload.append((model_app_label, model_name))
        super(RenameModelAndBaseOperation, self).state_forwards(app_label, state)
        state.reload_models(to_reload, delay=True)

class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0027_contributionvalue'),
        ('time_based', '0027_auto_20201110_1613'),

    ]

    operations = [
        migrations.RunSQL('DROP VIEW contributions;'),
        RenameModelAndBaseOperation('Contribution', 'Intention'),
    ]
