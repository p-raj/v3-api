#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import logging
from functools import reduce

from time import sleep

import requests
from mistralclient.api.v2.executions import ExecutionManager
from rest_framework import response, views
from rest_framework.permissions import AllowAny

from asap.apps.runtime.models.session import Session
from asap.libs.mistral.http_client import MistralHTTPClient

# TODO
MISTRAL_PROCESS_EXECUTION_NAME = 'process'

# TODO
PROCESS_SERVER = 'http://172.18.0.1:8000/'

logger = logging.getLogger(__name__)


def dot_to_json(a):
    # TODO
    # move to utils
    output = {}
    for key, value in a.items():
        path = key.split('.')
        if path[0] == 'json':
            path = path[1:]
        target = reduce(lambda d, k: d.setdefault(k, {}), path[:-1], output)
        target[path[-1]] = value
    return output


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

        username = ''
        if self.get_session():
            session = Session.objects.filter(uuid=self.get_session()).first()
            if session:
                username = session.author.username
            else:
                logger.debug('invalid session: %s', session)

        # FIXME
        # use AST instead of this hack
        data = json.loads(
            json.dumps(data)
                .replace('$.auth', username)
                .replace('$.session', self.get_session())
                .replace('$.widget', str(widget.uuid))
                .replace('$.process', self.kwargs.get('process_uuid'))
        )

        body = data.get(self.kwargs.get('process_uuid'), {})
        body.update(**request.data)

        em = ExecutionManager(MistralHTTPClient())
        if body.pop('__sync', None):
            workflow_data = dot_to_json(body)
            execution = em.create(
                workflow_data.get('workflow_name'),
                workflow_input=workflow_data.get('input', {})
            )

            while execution.state == 'RUNNING':
                # FIXME
                # wait for task completion
                # make it async :)
                sleep(1)
                execution = em.get(execution.id)

            result = json.loads(execution.output)
            logger.debug('workflow result: %s', result)
            return response.Response(
                data=result.get('data') or result.get('error'),
                status=result.get('status'),
                template_name=None,
                headers=result.get('headers')
            )

        else:
            resp = requests.post(
                self.get_process_url(**kwargs),
                json=body,
                params=dict(request.query_params)
            )

            data = resp.json()
            logger.debug('process response: %s', data)
            return response.Response(
                data=data,
                status=resp.status_code,
                template_name=None,
                headers=resp.headers
            )
