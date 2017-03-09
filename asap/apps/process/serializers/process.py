#!/usr/bin/python
# -*- coding: utf-8 -*-

from asap.apps.process.models import Process
from asap.core.serializers import TimestampableModelSerializer, AuthorableModelSerializer

from rest_framework import serializers


class ProcessSerializer(AuthorableModelSerializer, TimestampableModelSerializer,
                        serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Process
        exclude = ()

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            }
        }
