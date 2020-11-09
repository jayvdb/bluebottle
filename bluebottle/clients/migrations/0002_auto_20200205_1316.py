# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2020-02-05 12:16
from __future__ import unicode_literals

from django.db import migrations, connection


def create_update_function(apps, schema_editor):
    function_sql = """
        CREATE OR REPLACE FUNCTION refresh_union_view(table_name text) RETURNS void AS $$
        DECLARE
          schema TEXT;
          sql TEXT := '';
        BEGIN
          FOR schema IN SELECT schema_name FROM clients_client
          LOOP
            sql := sql || format('SELECT ''%I'' AS tenant, * FROM %I.%I UNION ALL ', schema, schema, table_name);
          END LOOP;

          EXECUTE
            format('CREATE OR REPLACE VIEW %I AS ', table_name) || left(sql, -11);
        END
        $$ LANGUAGE plpgsql;
    """

    if connection.tenant.schema_name == 'public':
        schema_editor.execute(function_sql, params=None)


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        ('donations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_update_function, migrations.RunPython.noop),
    ]
