import json
import logging
from time import sleep

import requests
from mistralclient.api.v2.executions import ExecutionManager
from rest_framework import response, views
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse_lazy

from asap.apps.runtime.models.session import Session
from asap.apps.widget.models.config import Config
from asap.libs.mistral.http_client import MistralHTTPClient
from asap.utils import dot_to_json
from asap.utils import transform
from asap.utils.parsers.plain_text import PlainTextParser

logger = logging.getLogger(__name__)


class WidgetProcessExecution(views.APIView):
    permission_classes = (AllowAny,)
    parser_classes = (
        PlainTextParser, FormParser,
        JSONParser, MultiPartParser
    )

    def get_session(self):
        return self.request.META.get('HTTP_X_VRT_SESSION', '')

    def get_process_url(self, request, **kwargs):
        return reverse_lazy(
            'process-execute',
            request=request,
            kwargs={
                'uuid': kwargs.get('action')
            }
        )

    def post(self, request, *args, **kwargs):
        logger.debug('content-type: %s', request.content_type)

        config = Config.objects.filter(
            widget__uuid=kwargs.get('widget_uuid'),
            process__uuid=kwargs.get('action')
        ).first()
        data = config.config or {} if config else {}
        logger.debug('widget config: %s', data)

        username = ''
        if self.get_session():
            session = Session.objects.filter(uuid=self.get_session()).first()
            if session:
                username = session.author.username
            else:
                logger.debug('invalid session: %s', session)

        # FIXME
        # use AST instead of this hack
        body = json.loads(
            json.dumps(data)
                .replace('$.auth', username)
                .replace('$.session', self.get_session())
                .replace('$.widget', kwargs.get('widget_uuid'))
                .replace('$.process', kwargs.get('action'))
        )
        body.update(**request.data)

        if config and config.transform:
            body = transform(body, config.transform.get('@request', {}))

        if body.get('workflow_name', None):
            em = ExecutionManager(MistralHTTPClient())
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

        resp = requests.post(
            self.get_process_url(request, **kwargs),
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
