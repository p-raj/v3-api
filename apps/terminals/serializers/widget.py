import json

from rest_framework import serializers

from ..models.widget import Widget


class WidgetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Widget
        fields = ['id', 'url', 'name', 'code']


class WidgetAdminSerializer(WidgetSerializer):
    config = serializers.SerializerMethodField()

    class Meta(WidgetSerializer.Meta):
        fields = ['id', 'url', 'name', 'code', 'config']

    def get_config(self, obj):
        return json.loads(obj.config)
