#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from rest_framework import response, viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny

from asap.apps.widget.models.widget import Widget
from asap.apps.widget.serializers.widget import WidgetSerializer
from asap.core.permissions.is_author_or_read_only import IsAuthorOrReadOnly
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin
from mistralclient.api.httpclient import HTTPClient
from mistralclient.api.v2.executions import ExecutionManager

logger = logging.getLogger(__name__)


class WidgetViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    permission_classes = (AllowAny,)

    lookup_field = 'uuid'
    lookup_parent = [
        ('widget_locker_uuid', 'widgetlocker__uuid')
    ]

    def get_queryset(self):
        queryset = super(WidgetViewSet, self).get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset

    def get_session_uuid(self):
        wsgi = getattr(self.request, '_request')
        return wsgi.META.get('HTTP_X_VRT_SESSION') or getattr(self, '_session', None)

    @detail_route(permission_classes=(AllowAny,))
    def execute(self, request, **kwargs):
        widget = self.get_object()
        session = self.get_session_uuid()

        from asap.apps.widget.views.process_service import MISTRAL_SERVER
        em = ExecutionManager(HTTPClient(MISTRAL_SERVER))
        execution = em.create(widget.workflow_uuid, workflow_input={
            'session': session
        })
        logger.info('widget execution id {0} for session {1}: '.format(execution.id, session))
        return response.Response()
