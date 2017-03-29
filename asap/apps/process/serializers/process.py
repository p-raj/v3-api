#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers

from asap.apps.process.models import Process
from asap.core.serializers import TimestampableModelSerializer


class ProcessSerializer(TimestampableModelSerializer,
                        serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Process
        exclude = ('author', )

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            }
        }
