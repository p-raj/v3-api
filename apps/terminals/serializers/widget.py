from rest_framework import serializers

from ..models.widget import Widget


class WidgetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Widget
        fields = ['id', 'url', 'name', 'code']
