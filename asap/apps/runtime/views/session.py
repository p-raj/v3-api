#!/usr/bin/python
# -*- coding: utf-8 -*-
import collections
import json

from rest_framework import response, viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse_lazy

from asap.apps.runtime.models.session import Session
from asap.apps.runtime.serializers.session import SessionSerializer
from asap.apps.widget.models.widget import Widget
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin


def flatten(d, parent_key='', sep='.'):
    """
    Credits: http://stackoverflow.com/a/6027615/1796173
    """
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# FIXME
# this is super ugly hack :/
# only AP know why, this one is definitely
# just for getting things done
# & it sucks big time
def expose_widget_data(data):
    for key in data.keys():
        # check if the key has further data
        if type(data[key]) != dict:
            # if not its neither a widget
            # nor a process :(
            continue

        # wp might be a widget or process
        # for processes data will always be empty :)
        wp = data[key]

        wd = {}
        for p in wp.keys():
            if type(wp[p]) != dict:
                # if not its neither a widget
                # nor a process :(
                continue
            # we are quite sure we have hit a process
            pd = wp[p].get('data', {})
            wdd = wd.get('data', {})
            wdd.update(**pd)
            wd.update({
                'data': wdd
            })

        if wd:
            data[key]['data'] = flatten(wd)


class SessionViewSet(AuthorableModelViewSet, DRFNestedViewMixin,
                     viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = (AllowAny,)

    lookup_field = 'uuid'
    lookup_parent = [
        ('runtime_uuid', 'runtime__uuid')
    ]

    def create(self, request, *args, **kwargs):
        self.filter_nested_queryset(**kwargs)
        if self.is_nested:
            # we don't need to ask for the runtime to which the
            # session will be associated when the url is nested
            request.data.update(runtime=reverse_lazy('runtime-detail', kwargs={
                'uuid': kwargs.get('runtime_uuid')
            }))
        return super(SessionViewSet, self).create(request, *args, **kwargs)

    def get_object(self):
        instance = super(SessionViewSet, self).get_object()

        # not saving the timestamp just doing it for the client,
        # we'll remove this @ first sign of trouble :P
        data = instance.data or {}
        data.update(last_modified=instance.modified_at.timestamp())

        # FIXME
        # mutate session data
        expose_widget_data(data)

        instance.data = data
        return instance

    @detail_route(permission_classes=[AllowAny], methods=['post'])
    def set(self, request, *args, **kwargs):
        data = request.data
        data = data if type(data) == dict else json.loads(data)
        data = {
            request.META.get('HTTP_PROCESS', 'invalid'): data
        }

        instance = self.get_object()
        instance.data.update(**data)
        instance.save()
        return self.retrieve(request, *args, **kwargs)

    @detail_route(permission_classes=[AllowAny], methods=['get', 'post'])
    def get(self, request, **kwargs):
        widget = request.META.get('HTTP_WIDGET', 'invalid')
        process = request.META.get('HTTP_PROCESS', 'invalid')
        instance = self.get_object()

        # FIXME
        # if the requesting process is a part of
        # rule, return trigger data
        # very very very ugly again :'(
        # not cool :'(
        # missing widget info!!
        widget = Widget.objects.filter(uuid=widget).first()
        if not widget:
            return response.Response({})

        triggers = [r.get('trigger', {}).get('uuid')
                    for r in widget.rules
                    if r.get('action', {}).get('uuid') == process]
        if not triggers:
            return response.Response(instance.data.get(process, {}))

        data = {}
        # FIXME
        # missing widget info!!
        # combine all widget data for the triggers :'( :'(
        for trigger in triggers:
            data.update(**instance.data.get(trigger, {}))
        return response.Response(data)
