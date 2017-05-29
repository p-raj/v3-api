#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import requests
from django.urls import reverse_lazy

from rest_framework import serializers

from asap.apps.widget.models.widget import Widget
from asap.core.serializers import TimestampableModelSerializer

swagger_dict = {
    'swagger': '2.0',
    'info': {
        'title': '',
        'version': '1.0.0'
    },
    'paths': {},
    'definitions': {},
    'securityDefinitions': {}
}


class WidgetSerializer(TimestampableModelSerializer, serializers.HyperlinkedModelSerializer):
    schema = serializers.SerializerMethodField()

    class Meta:
        model = Widget
        exclude = ('author', 'is_published')

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            }
        }

    def get_schema(self, obj):
        # move these lame tasks to some place else
        # and make these smart
        schema = copy.deepcopy(swagger_dict)

        # update the open API spec title to match the widget uuid
        schema.get('info').update(title=str(obj.uuid))

        # copy the path that the process represents
        # change the path
        for process in obj.processes:
            process_server = reverse_lazy('process-server', kwargs={
                'uuid': str(process.uuid)
            })

            process_schema = requests.get('http://172.20.0.1:8000' + str(process_server)).json()
            widget_proxy = reverse_lazy('widget-process-proxy', kwargs={
                'uuid': str(obj.uuid),
                'process_uuid': process.uuid
            })
            schema['paths'][str(widget_proxy)] = process_schema.get('paths') \
                .get('/api/v1/processes/{0}/execute/'.format(process.uuid))
        return schema
