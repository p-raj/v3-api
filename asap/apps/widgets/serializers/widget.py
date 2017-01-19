#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- widgets.serializers.widget
~~~~~~~~~~~~~~

- This file contains the Widget Serializers that will help in rendering Widget Response and validating upcoming
   http request.
 """

# future
from __future__ import unicode_literals


# DRF
from rest_framework import serializers

# local
from asap.core.serializers import TimestampableModelSerializer

# own app
from asap.apps.widgets.models.widget import Widget


class WidgetSerializer(TimestampableModelSerializer, serializers.ModelSerializer):
    """Widget Serializer

    """

    # Meta
    class Meta:
        model = Widget
        exclude = ('author',)

        extra_kwargs = {
            'url': {
                'lookup_field': 'token'
            }
        }
