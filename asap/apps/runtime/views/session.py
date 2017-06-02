#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import logging

from rest_framework import response, viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse_lazy

from asap.apps.runtime.models.session import Session, STATE_SUCCESS, STATE_CANCELLED
from asap.apps.runtime.serializers.session import SessionSerializer
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin
from asap.core.views.version import VersionableModelViewSet

logger = logging.getLogger(__name__)


class SessionViewSet(AuthorableModelViewSet, DRFNestedViewMixin,
                     VersionableModelViewSet, viewsets.ModelViewSet):
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

        # FIXME
        # not saving the timestamp just doing it for the client,
        # we'll remove this @ first sign of trouble :P
        data = instance.data or {}
        data.update(last_modified=instance.modified_at.timestamp())

        instance.data = data
        return instance

    @detail_route(permission_classes=[AllowAny], methods=['post'])
    def write(self, request, *args, **kwargs):
        instance = self.get_object()

        logger.debug('session %s', instance)

        data = request.data
        data = data if type(data) == dict else json.loads(data)
        data = {
            data.get('key', 'invalid'): data.get('data', {})
        }

        logger.debug('write %s', data)
        instance.data.update(**data)
        instance.save()
        return self.retrieve(request, *args, **kwargs)

    @detail_route(permission_classes=[AllowAny], methods=['post'])
    def read(self, request, **kwargs):
        key = request.data.get('key', 'invalid')
        instance = self.get_object()
        logger.debug('session %s', instance)

        data = instance.data.get(key, {})
        logger.debug('read %s', data)
        return response.Response(data)

    @detail_route(methods=['post'])
    def success(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.state = STATE_SUCCESS
        instance.save()
        return self.retrieve(request, *args, **kwargs)

    @detail_route(methods=['post'])
    def cancel(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.state = STATE_CANCELLED
        instance.save()
        return self.retrieve(request, *args, **kwargs)
