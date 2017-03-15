#!/usr/bin/python
# -*- coding: utf-8 -*-

from asap.apps.process.models import ProcessLocker
from asap.core.serializers import TimestampableModelSerializer, AuthorableModelSerializer

from rest_framework import serializers


class ProcessLockerSerializer(AuthorableModelSerializer, TimestampableModelSerializer,
                              serializers.HyperlinkedModelSerializer):
    token = serializers.CharField()

    class Meta:
        model = ProcessLocker
        exclude = ()

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            },
            'processes': {
                'lookup_field': 'uuid'
            }
        }
