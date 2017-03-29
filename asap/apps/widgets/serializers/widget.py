#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import requests
from django.urls import reverse_lazy

from rest_framework import serializers

from asap.apps.widgets.models.widget import Widget
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
        exclude = ('author', 'processes_json',)
        read_only_fields = ('processes_json',)

        extra_kwargs = {
            'url': {
                'lookup_field': 'uuid'
            }
        }

    def get_schema(self, obj):
        # move these lame tasks to some place else
        # and make these smart
        processes = obj.processes_json

        if not processes or type(processes) == dict:
            return processes

        schema = copy.deepcopy(swagger_dict)

        # update the open API spec title to match the widget uuid
        schema.get('info').update(title=str(obj.uuid))

        # copy the path that the process represents
        # change the path
        for p in processes:
            resp = requests.get('{0}server/'.format(p.get('url')))
            process_schema = resp.json()
            widget_proxy = reverse_lazy('widget-process-proxy', kwargs={
                'uuid': str(obj.uuid),
                'process_uuid': p.get('uuid')
            })
            schema['paths'][str(widget_proxy)] = process_schema.get('paths') \
                .get('/api/v1/processes/{0}/execute/'.format(p.get('uuid')))
        return schema
