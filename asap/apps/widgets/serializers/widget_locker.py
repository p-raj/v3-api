#!/usr/bin/python
# -*- coding: utf-8 -*-

from asap.apps.widgets.models.widget_locker import WidgetLocker
from asap.core.serializers import TimestampableModelSerializer

from rest_framework import serializers


class WidgetLockerSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WidgetLocker
        exclude = ('author',)

        extra_kwargs = {
            'url': {
                'lookup_field': 'token'
            },
            'widgets': {
                'lookup_field': 'token'
            }
        }
