import json

from apps.terminals.serializers.widget import WidgetSerializer
from rest_framework import serializers

from ..models import WidgetContainer


class WidgetContainerSerializer(serializers.HyperlinkedModelSerializer):
    widget = WidgetSerializer()
    config = serializers.SerializerMethodField()

    class Meta:
        model = WidgetContainer
        fields = ['id', 'url', 'screen', 'widget', 'order',
                  'is_required', 'config']

    def get_config(self, obj):
        container_config = json.loads(obj.config)
        original_config = json.loads(obj.widget.config)

        config = original_config.get('public')
        config.update(**container_config)
        return config
