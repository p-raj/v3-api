import json

from django.conf import settings
from rest_framework import serializers, fields
from reversion.models import Version, Revision

DATETIME_FORMAT = getattr(settings, 'DATETIME_FORMAT', '%Y-%m-%dT%H:%M:%S%z')


class AuthorableModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer Mixin for models using Authorable Mixins.
    """
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        """
        :param obj:
        :return:
        """
        return obj.username


class TimestampableModelSerializer(serializers.ModelSerializer):
    """
    Serializer Mixin for models using Timestampable Mixins.
    """
    # strip off milli seconds,
    # some clients don't handle this properly :/
    created_at = serializers.DateTimeField(read_only=True, format=DATETIME_FORMAT)
    modified_at = serializers.DateTimeField(read_only=True, format=DATETIME_FORMAT)


class RevisionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Revision
        fields = '__all__'


class VersionSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)

    serialized_data = fields.SerializerMethodField()
    revision = RevisionSerializer()

    @staticmethod
    def get_serialized_data(obj):
        return json.loads(obj.serialized_data)

    class Meta:
        model = Version
        exclude = ('content_type',)
