#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import response, viewsets
from rest_framework.decorators import detail_route

from asap.apps.widgets.models.widget import Widget
from asap.apps.widgets.serializers.widget import WidgetSerializer
from asap.core.permissions.is_author_or_read_only import IsAuthorOrReadOnly
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin
from mistralclient.api.httpclient import HTTPClient
from mistralclient.api.v2.executions import ExecutionManager


class WidgetViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    lookup_field = 'uuid'
    lookup_parent = [
        ('widget_locker_token', 'widgetlocker__token')
    ]

    def get_session_uuid(self):
        wsgi = getattr(self.request, '_request')
        return wsgi.META.get('HTTP_X_VRT_SESSION') or getattr(self, '_session', None)

    @detail_route()
    def execute(self, request, **kwargs):
        widget = self.get_object()
        session = self.get_session_uuid()

        from asap.apps.widgets.views.process_service import MISTRAL_SERVER
        em = ExecutionManager(HTTPClient(MISTRAL_SERVER))
        execution = em.create(widget.workflow_uuid, workflow_input={
            'session': session,
            'callback': ''
        })

        return response.Response()
