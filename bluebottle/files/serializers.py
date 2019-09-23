import os

from django.core.urlresolvers import reverse
from rest_framework import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from rest_framework_json_api.serializers import ModelSerializer

from bluebottle.files.models import Document, Image
from bluebottle.utils.utils import reverse_signed


class DocumentField(ResourceRelatedField):
    def get_queryset(self):
        return Document.objects.all()


class FileSerializer(ModelSerializer):
    file = serializers.FileField(write_only=True)
    filename = serializers.SerializerMethodField()
    owner = ResourceRelatedField(read_only=True)
    size = serializers.IntegerField(read_only=True, source='file.size')

    included_serializers = {
        'owner': 'bluebottle.initiatives.serializers.MemberSerializer',
    }

    class Meta:
        model = Document
        fields = ('id', 'file', 'filename', 'size', 'owner', )
        meta_fields = ['size', 'filename']

    class JSONAPIMeta:
        included_resources = ['owner', ]

    def get_filename(self, instance):
        return os.path.basename(instance.file.name)


class DocumentSerializer(ModelSerializer):
    file = serializers.FileField(write_only=True)
    filename = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()
    owner = ResourceRelatedField(read_only=True)
    size = serializers.IntegerField(read_only=True, source='file.size')

    included_serializers = {
        'owner': 'bluebottle.initiatives.serializers.MemberSerializer',
    }

    def get_link(self, obj):
        parent_id = getattr(obj, self.relationship).get().pk
        return reverse(self.content_view_name, args=(parent_id,))

    def get_filename(self, instance):
        return os.path.basename(instance.file.name)

    class Meta:
        model = Document
        fields = ('id', 'file', 'filename', 'size', 'owner', 'link',)
        meta_fields = ['size', 'filename']

    class JSONAPIMeta:
        included_resources = ['owner', ]


class PrivateDocumentSerializer(DocumentSerializer):

    def get_link(self, obj):
        parent_id = getattr(obj, self.relationship).get().pk
        return reverse_signed(self.content_view_name, args=(parent_id, ))


class ImageField(ResourceRelatedField):
    def get_queryset(self):
        return Image.objects.all()


class ImageSerializer(DocumentSerializer):
    links = serializers.SerializerMethodField()

    def get_links(self, obj):
        if hasattr(self, 'sizes'):
            parent_id = getattr(obj, self.relationship).get().pk
            return dict(
                (
                    key,
                    reverse(self.content_view_name, args=(parent_id, size))
                ) for key, size in self.sizes.items()
            )

    class Meta:
        model = Image
        fields = ('id', 'file', 'filename', 'size', 'owner', 'links',)
        meta_fields = ['size', 'filename']
