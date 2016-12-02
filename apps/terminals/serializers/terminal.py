from rest_framework import serializers

from ..models import Terminal


class TerminalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Terminal
        fields = ['id', 'url', 'name']
