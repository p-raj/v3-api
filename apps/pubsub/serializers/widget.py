import json

from apps.pubsub.models.widget import Widget
from rest_framework import serializers


class WidgetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Widget
        fields = ['id', 'url', 'name', 'code']


class WidgetAdminSerializer(WidgetSerializer):
    config = serializers.SerializerMethodField()

    class Meta(WidgetSerializer.Meta):
        fields = ['id', 'url', 'name', 'code', 'config']

    def get_config(self, obj):
        return json.loads(obj.config) if obj.config else None
