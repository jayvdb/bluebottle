# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Location.zoom_level'
        db.delete_column(u'geo_location', 'zoom_level')

        # Deleting field 'Location.longitude'
        db.delete_column(u'geo_location', 'longitude')

        # Deleting field 'Location.latitude'
        db.delete_column(u'geo_location', 'latitude')

        # Adding field 'Location.position'
        db.add_column(u'geo_location', 'position',
                      self.gf('geoposition.fields.GeopositionField')(max_length=42, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Location.zoom_level'
        db.add_column(u'geo_location', 'zoom_level',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Location.longitude'
        db.add_column(u'geo_location', 'longitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=21, decimal_places=18, blank=True),
                      keep_default=False)

        # Adding field 'Location.latitude'
        db.add_column(u'geo_location', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=21, decimal_places=18, blank=True),
                      keep_default=False)

        # Deleting field 'Location.position'
        db.delete_column(u'geo_location', 'position')


    models = {
        u'geo.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'alpha2_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'alpha3_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'oda_recipient': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subregion': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geo.SubRegion']"})
        },
        u'geo.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('geoposition.fields.GeopositionField', [], {'max_length': '42', 'null': 'True'})
        },
        u'geo.region': {
            'Meta': {'ordering': "['name']", 'object_name': 'Region'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'geo.subregion': {
            'Meta': {'ordering': "['name']", 'object_name': 'SubRegion'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geo.Region']"})
        }
    }

    complete_apps = ['geo']