#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers

from asap.apps.widget.models.widget import Widget
from asap.core.serializers import TimestampableModelSerializer


class WidgetSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    schema = serializers.ReadOnlyField()

    class Meta:
        model = Widget
        exclude = ('author', 'is_published',)

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            },
            'processes': {
                'lookup_field': 'uuid'
            }
        }
