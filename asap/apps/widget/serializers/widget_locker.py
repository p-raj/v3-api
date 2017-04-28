#!/usr/bin/python
# -*- coding: utf-8 -*-

from asap.apps.widget.models.widget import Widget
from asap.apps.widget.models.widget_locker import WidgetLocker
from asap.apps.widget.serializers.widget import WidgetSerializer
from asap.core.serializers import TimestampableModelSerializer

from rest_framework import serializers

from asap.fields.hyperlinked_serialized_related_field import HyperlinkedSerializedRelatedField


class WidgetLockerSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    token = serializers.CharField(read_only=True)
    widgets = HyperlinkedSerializedRelatedField(
        view_name='widget-detail', many=True,
        serializer=WidgetSerializer,
        queryset=Widget.objects.all(),
        style={
            'base_template': 'input.html'
        },
        lookup_field='uuid'
    )

    class Meta:
        model = WidgetLocker
        exclude = ('author',)

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            },
            'widgets': {
                'lookup_field': 'uuid'
            }
        }
