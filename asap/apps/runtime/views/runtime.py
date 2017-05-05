#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from mistralclient.api.v2.executions import ExecutionManager
from rest_framework import response, viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny

from asap.apps.runtime.models.runtime import Runtime
from asap.apps.runtime.serializers.runtime import RuntimeSerializer
from asap.core.filters.am_filter import AMFilter
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin
from asap.libs.mistral.http_client import MistralHTTPClient

logger = logging.getLogger(__name__)


class RuntimeViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Runtime.objects.all()
    serializer_class = RuntimeSerializer
    filter_backends = (AMFilter,)

    lookup_field = 'uuid'
    lookup_parent = [
        ('runtime_locker_uuid', 'runtimelocker__uuid')
    ]

    def get_session_uuid(self):
        wsgi = getattr(self.request, '_request')
        return wsgi.META.get('HTTP_X_VRT_SESSION') or getattr(self, '_session', None)

    @detail_route(permission_classes=(AllowAny,))
    def execute(self, request, **kwargs):
        runtime = self.get_object()
        session = self.get_session_uuid()

        em = ExecutionManager(MistralHTTPClient())
        execution = em.create(runtime.workflow_uuid, workflow_input={
            'session': session
        }, task_name='wait_for_widgets')
        logger.info('runtime execution id {0} for session {1}: '.format(execution.id, session))
        return response.Response()
