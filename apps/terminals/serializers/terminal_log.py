from rest_framework import serializers

from ..models import TerminalLog


class TerminalLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TerminalLog
        fields = ['id', 'url', 'terminal', 'data']
