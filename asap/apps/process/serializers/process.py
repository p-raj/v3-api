#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers

from asap.apps.process.models import Process
from asap.apps.process.schema.validator import SchemaValidator
from asap.core.serializers import TimestampableModelSerializer


class ProcessSerializer(TimestampableModelSerializer,
                        serializers.HyperlinkedModelSerializer):
    schema = serializers.JSONField(validators=[
        SchemaValidator()
    ])

    class Meta:
        model = Process
        exclude = ('author', 'is_system')

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            }
        }
