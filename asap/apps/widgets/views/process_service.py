#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from time import sleep

from rest_framework import response, views

from mistralclient.api.httpclient import HTTPClient
from mistralclient.api.v2.executions import ExecutionManager

# TODO
MISTRAL_SERVER = 'http://localhost:8989/v2'
MISTRAL_PROCESS_EXECUTION_NAME = 'process'

# TODO
PROCESS_SERVER = 'http://172.19.0.1:8001/'


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
    proxy_host = 'http://localhost:8000'
    source = 'api/v1/processes/%(process_uuid)s/execute/'

    @staticmethod
    def get_process_url(**kwargs):
        return '{process_server}{path}'.format(**{
            'process_server': PROCESS_SERVER,
            'path': 'api/v1/processes/%(process_uuid)s/execute/'
        }) % kwargs

    @staticmethod
    def get_authorization_header(**kwargs):
        from asap.apps.widgets.models.widget import Widget
        widget = Widget.objects.get(uuid=kwargs.get('uuid'))
        return widget.process_locker_token

    def post(self, request, *args, **kwargs):
        raw_request = getattr(request, '_request')
        em = ExecutionManager(HTTPClient(MISTRAL_SERVER))
        execution = em.create(MISTRAL_PROCESS_EXECUTION_NAME, workflow_input={
            'url': self.get_process_url(**kwargs),
            'method': 'post',
            'params': dict(request.query_params),
            'body': request.data,
            'cookies': raw_request.COOKIES,
            'headers': {
                'Content-Type': request.content_type,
                'Authorization': self.get_authenticate_header(kwargs)
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
