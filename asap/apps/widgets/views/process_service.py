#!/usr/bin/python
# -*- coding: utf-8 -*-

import uuid

from rest_framework.permissions import AllowAny
from rest_framework_proxy.views import ProxyView

from asap.apps.logs.logging import ServiceLogging
from asap.apps.widgets.models.widget import Widget


class LoggingProxyViewSet(ProxyView):
    """

    """
    # TODO : remove AllowAny permission with proper permission class
    permission_classes = (AllowAny,)

    logger = None
    session = uuid.uuid4()
    actor = 'widget'

    def __init__(self, **kwargs):
        super(LoggingProxyViewSet, self).__init__(**kwargs)
        self.widget_uuid = None
        self.process_uuid = None

    def _init_logger_(self, request, token):
        """
        :param request : Django request object.
        :param token : process token, helps in identifying the process
        :return: logging class instance
        """
        self.logger = ServiceLogging(
            self.actor, token, self.session,
            payload=request.data or dict()
        )

    def create_response(self, response):
        _response = response
        self.logger.handshake_succeed(self.process_uuid, None, response)
        response = super(LoggingProxyViewSet, self).create_response(response)

        if response.status_code >= 400:
            try:
                response.data = _response.json()
            except Exception as e:
                # let's log to check when it fails
                # TODO: use logger
                print(e)

        # payload gets overridden anyways in logger._log_db_entry
        # so why bother sending it ?
        # remove the parameter from the method signature
        self.logger.success(response)  # logged as success
        return response

    def create_error_response(self, body, status):
        self.logger.handshake_failed(self.process_uuid, None, status, body)
        response = super(LoggingProxyViewSet, self).create_error_response(body, status)

        # payload gets overridden anyways in logger._log_db_entry
        # so why bother sending it ?
        # remove the parameter from the method signature
        self.logger.fail(response)  # logged as failure
        return response

    def proxy(self, request, *args, **kwargs):
        self.widget_uuid = kwargs.get('uuid')
        self.process_uuid = kwargs.get('process_uuid')

        widget = Widget.objects.filter(token=self.widget_uuid).first()
        if widget and widget.data:
            # update request data ?
            # doesn't seem like a good solution
            # but we are just a proxy ?
            # does proxies add data ? maybe.
            # TODO
            # seems fishy
            request.data.update(**widget.data)

        if self.logger is None:
            self._init_logger_(request, self.widget_uuid)

        self.logger.initialize()
        self.logger.handshake(self.process_uuid, request.data)
        return super(LoggingProxyViewSet, self).proxy(request, *args, **kwargs)


class ProcessActionProxyViewSet(LoggingProxyViewSet):
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

    def get_headers(self, request):
        # django.core.handlers.wsgi.WSGIRequest
        req = getattr(request, '_request')
        auth_header = req.META.get('HTTP_AUTHORIZATION')

        headers = super(ProcessActionProxyViewSet, self).get_headers(request)
        if auth_header:
            # FIXME:
            # obtain the authorization from the widget schema :)
            headers['AUTHORIZATION'] = auth_header

        return headers
