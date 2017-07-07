#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from rest_framework import viewsets, response
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny

from asap.apps.runtime.models.runtime import Runtime
from asap.apps.runtime.models.session import Session
from asap.apps.widget.models.widget import Widget
from asap.apps.widget.serializers.widget import WidgetSerializer
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin

logger = logging.getLogger(__name__)


class WidgetViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer

    lookup_field = 'uuid'
    lookup_parent = [
        ('app_uuid', 'widget_runtime_runtime__uuid')
    ]
    lookup_fields = (
        'name', 'description'
    )
    ordering_fields = (
        'created_at', 'modified_at'
    )

    def make_queryset(self):
        queryset = self.get_queryset()
        if not self.is_nested and \
                self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset

    @list_route(permission_classes=(AllowAny,))
    def system(self, request, *args, **kwargs):
        instance = self.queryset.filter(name='__system__').first()
        serializer = self.get_serializer_class()(
            instance=instance,
            context={
                'request': request
            }
        )
        return response.Response(serializer.data)

    def list(self, request, *args, **kwargs):
        resp = super(WidgetViewSet, self).list(request, *args, **kwargs)
        if not self.is_nested:
            return resp

        self.check_session()
        resp['X-VRT-SESSION'] = self.get_session_uuid()
        return resp

    def get_session_uuid(self):
        wsgi = getattr(self.request, '_request')
        return wsgi.META.get('HTTP_X_VRT_SESSION') or getattr(self, '_session', None)

    def check_session(self):
        session_uuid = self.get_session_uuid()
        if session_uuid:
            return Session.objects.filter(uuid=session_uuid).first()

        runtime = Runtime.objects.filter(
            uuid=self.kwargs.get('app_uuid')
        ).first()
        session = Session.objects.create(
            author=self.request.user, runtime=runtime
        )
        setattr(self, '_session', session.uuid)
        return session
