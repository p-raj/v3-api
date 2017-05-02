#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from rest_framework import response, viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse_lazy

from asap.apps.runtime.models.session import Session
from asap.apps.runtime.serializers.session import SessionSerializer
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin


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
        instance = self.get_object()
        return response.Response(instance.data.get(request.META.get('HTTP_PROCESS', 'invalid'), {}))
