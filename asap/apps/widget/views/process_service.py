#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import logging

from time import sleep

from mistralclient.api.v2.executions import ExecutionManager
from rest_framework import response, views
from rest_framework.permissions import AllowAny

from asap.libs.mistral.http_client import MistralHTTPClient

# TODO
MISTRAL_PROCESS_EXECUTION_NAME = 'process'

# TODO
PROCESS_SERVER = 'http://172.19.0.1:8000/'
KEYSTORE_SERVER = 'http://172.19.0.1:8000/api/v1/sessions'

logger = logging.getLogger(__name__)


class ProcessActionProxyViewSet(views.APIView):
    """
    A Proxy ViewSet to fetch data from the Processes Service
    while maintaining a session.

    Example:
        - `/widgets/<w_id>/process/` should internally call
            `/widget-lockers/<wl_id>/process/` and start a session for the `Widget`.
        - `/widgets/<w_id>/process/<p_id>/` should internally call
            `/process/<p_id>/` and update the session for the `Widget`.
    """

    permission_classes = (AllowAny,)

    def get_session(self):
        return self.request.META.get('HTTP_X_VRT_SESSION', '')

    def get_process_url(self, **kwargs):
        # direct
        return '{process_server}{path}'.format(**{
            'process_server': PROCESS_SERVER,
            'path': 'api/v1/processes/%(process_uuid)s/execute/'
        }) % kwargs

    def post(self, request, *args, **kwargs):
        raw_request = getattr(request, '_request')
        logger.debug('content-type: %s', request.content_type)

        from asap.apps.widget.models.widget import Widget
        widget = Widget.objects.get(uuid=kwargs.get('uuid'))
        logger.debug('widget: %s', widget)
        data = widget.data or {}
        logger.debug('widget data: %s', data)

        # FIXME
        # use AST instead of this hack
        data = json.loads(
            json.dumps(data)
                .replace('$.session', self.get_session())
                .replace('$.widget', str(widget.uuid))
                .replace('$.process', self.kwargs.get('process_uuid'))
        )

        body = data.get(self.kwargs.get('process_uuid'), {})
        body.update(**request.data)

        em = ExecutionManager(MistralHTTPClient())
        execution = em.create(MISTRAL_PROCESS_EXECUTION_NAME, workflow_input={
            'url': self.get_process_url(**kwargs),
            'method': 'post',
            'params': dict(request.query_params),
            'body': body,
            'cookies': raw_request.COOKIES,
            'headers': {
                'Content-Type': 'application/json',
                'Authorization': widget.process_locker_token,
                'Process': kwargs.get('process_uuid'),
                'Widget': kwargs.get('uuid')
            }
        })

        while execution.state == 'RUNNING':
            # FIXME
            # wait for task completion
            # make it async :)
            sleep(1)
            execution = em.get(execution.id)

        result = json.loads(execution.output)
        return response.Response(
            data=result.get('data') or result.get('error'),
            status=result.get('status'),
            template_name=None,
            headers=result.get('headers')
        )
