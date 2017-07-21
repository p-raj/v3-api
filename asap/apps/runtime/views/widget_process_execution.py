import json
import logging
from time import sleep

import requests
from box import Box
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

    def post(self, request, *args, **kwargs):
        logger.debug('content-type: %s', request.content_type)
        body = self.get_action_data(request, *args, **kwargs)

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
            self.get_process_url(request, kwargs.get('action')),
            json=body, params=dict(request.query_params)
        )

        data = resp.json()
        logger.debug('process response: %s', data)
        return response.Response(
            data=data,
            status=resp.status_code,
            template_name=None,
            headers=resp.headers
        )

    def get_action_data(self, request, *args, **kwargs):
        if not request.content_type.startswith('application/json'):
            return request.data

        # FIXME
        # use AST instead of this hack
        # replace variables, for backward compatibility
        # YAQL should take care of it in future
        data = json.loads(
            json.dumps(self.data)
                .replace('$.auth', self.user.username)
                .replace('$.session', self.session)
                .replace('$.widget', self.environment.widget)
                .replace('$.process', self.environment.process)
        )

        if not self.expressions:
            # for backwards compatibility
            d = data.get('@config')
            d.update(**data.get('@context'))
            return d

        return transform(data, self.expressions)

    # noinspection PyAttributeOutsideInit
    def initial(self, request, *args, **kwargs):
        super(WidgetProcessExecution, self).initial(request, *args, **kwargs)

        # Runs anything that needs to occur prior to calling
        # the method handler :)

        # session is a pre-requisite
        self.session = self.request.META.get('HTTP_X_VRT_SESSION', '')
        # there are a lot of places where session is not yet compulsory :/
        # so let's just log it
        logger.debug('session: %s', self.session)
        # assert not self.session, 'session not provided, ' \
        #                          'consider sending a valid X-VRT-SESSION header'

        # the viewset is unprotected to be used as a workflow callback :/
        # so for now we need to have the user determined by the session
        # instead of the request.
        # FIXME
        self.user = request.user
        if self.session:
            session = Session.objects.filter(uuid=self.session).first()
            self.user = session.author
            # assert not self.user.is_authenticated(), 'user must authenticated'
            logger.debug('req user: %s', request.user)
            logger.debug('session user: %s', self.user)

        # the data available can be divided in 3 parts
        # context       - data from the client: eg. user input, & user information
        #               the context will only be set if the content-type is application/json
        # environment   - info like widget/process/session
        # configuration - data saved in the widget config,
        #               used for storing sensitive info like secrets
        self.context = request.data \
            if request.content_type.startswith('application/json') \
            else {}

        widget = kwargs.get('widget_uuid')
        process = kwargs.get('action')
        self.environment = Box({
            'widget': widget,
            'process': process,
            'session': self.session
        })

        config = Config.objects.filter(
            widget__uuid=widget,
            process__uuid=process
        ).first()
        self.config = config.config or {} if config else {}

        self.data = {
            '@context': self.context,
            '@config': self.config,
            '@env': self.environment,
        }

        # TODO
        # separate expression for req/resp
        self.expressions = config.transform or {}

    @staticmethod
    def get_process_url(request, process_id):
        return reverse_lazy(
            'process-execute',
            request=request,
            kwargs={
                'uuid': process_id
            }
        )
