#!/usr/bin/python
# -*- coding: utf-8 -*-

from asap.apps.widgets.models.widget import Widget
from asap.core.serializers import TimestampableModelSerializer

from rest_framework import serializers


class WidgetSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Widget
        exclude = ('author',)

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            }
        }
