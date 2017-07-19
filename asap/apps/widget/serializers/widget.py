#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers

from asap.apps.widget.models.widget import Widget
from asap.core.serializers import TimestampableModelSerializer


class WidgetSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    schema = serializers.ReadOnlyField()

    # TODO
    # Multiple Serializers based on permissions/clients
    # config should not be sent to client

    class Meta:
        model = Widget
        exclude = ('author', 'is_published', 'process_configs')

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            },
            'processes': {
                'lookup_field': 'uuid'
            }
        }
