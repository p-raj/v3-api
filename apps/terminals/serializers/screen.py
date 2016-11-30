from apps.terminals.serializers.widget_container import WidgetContainerSerializer
from rest_framework import serializers

from ..models import Screen


class ScreenSerializer(serializers.HyperlinkedModelSerializer):
    widgets = WidgetContainerSerializer(source='widgetcontainer_set', many=True)

    class Meta:
        model = Screen
        fields = ['id', 'url', 'name', 'help_text', 'order',
                  'widgets']
