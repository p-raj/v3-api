#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers

from asap.apps.process.models import ProcessLocker
from asap.apps.process.models.process import Process
from asap.apps.process.serializers.process import ProcessSerializer
from asap.core.serializers import AuthorableModelSerializer, TimestampableModelSerializer
from asap.fields.hyperlinked_serialized_related_field import HyperlinkedSerializedRelatedField


class ProcessLockerSerializer(AuthorableModelSerializer, TimestampableModelSerializer,
                              serializers.HyperlinkedModelSerializer):
    token = serializers.CharField(read_only=True)
    processes = HyperlinkedSerializedRelatedField(
        view_name='process-detail', many=True,
        serializer=ProcessSerializer,
        queryset=Process.objects.all(),
        style={
            'base_template': 'input.html'
        },
        lookup_field='uuid'
    )

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
