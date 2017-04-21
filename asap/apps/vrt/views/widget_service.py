#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from django.core.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework_proxy.views import ProxyView

from asap.apps.vrt.models.runtime import Runtime
from asap.apps.vrt.models.session import Session

logger = logging.getLogger(__name__)


class SessionMixin(ProxyView):
    """

    """
    # the session can't be initiated
    # in the middle of runtime calls
    # for instance the widgets rendering API may start a new session
    # but the a widget action shouldn't initiate a session
    # a widget action must provide a session id
    # so a runtime session may be resumed
    allow_new = None

    def get_allow_new(self):
        return self.allow_new

    def get_session_uuid(self):
        wsgi = getattr(self.request, '_request')
        return wsgi.META.get('HTTP_X_VRT_SESSION') or getattr(self, '_session', None)

    def get_session(self):
        session_uuid = self.get_session_uuid()
        if session_uuid:
            return Session.objects.filter(uuid=session_uuid).first()

        if self.get_allow_new():
            runtime = Runtime.objects.filter(uuid=self.runtime_uuid).first()
            session = Session.objects.create(author=self.request.user, data={}, runtime=runtime)
            setattr(self, '_session', session.uuid)
            return session
        return None

    def update_session(self, key, value):
        # a proxy can't be created if the session is not known
        # session will either be created when fetching widgets info
        # or through a separate initialization
        # subjected to change :D
        session = self.get_session()

        if not session:
            raise PermissionDenied

        session.data.update(**{
            key: value
        })
        session.save()


class WidgetProxyViewSet(SessionMixin, ProxyView):
    """
    A Proxy ViewSet to fetch data from the Widgets Service
    while maintaining a session.

    Example:
        - `/runtimes/<r_id>/widgets/` should internally call
            `/widget-lockers/<wl_id>/widgets/` and start a session for the `Runtime`.
        - `/runtimes/<r_id>/widgets/<w_id>/` should internally call
            `/widgets/<w_id>/` and update the session for the `Runtime`.
    """

    permission_classes = (AllowAny,)

    def get_source_path(self):
        runtime = Runtime.objects.filter(uuid=self.kwargs.get('uuid')).first()
        if not runtime or not runtime.widget_locker_uuid:
            return None

        # get source path maps the kwargs to the path
        # let's add widget_locker_uuid to it
        self.kwargs.update(widget_locker_uuid=runtime.widget_locker_uuid)
        return super(WidgetProxyViewSet, self).get_source_path()


class WidgetListProxyViewSet(WidgetProxyViewSet):
    """
    A Proxy ViewSet to fetch data from the Widgets Service
    while maintaining a session.

    Example:
        - `/runtimes/<r_id>/widgets/` should internally call
            `/widget-lockers/<wl_id>/widgets/` and start a session for the `Runtime`.
        - `/runtimes/<r_id>/widgets/<w_id>/` should internally call
            `/widgets/<w_id>/` and update the session for the `Runtime`.
    """
    allow_new = True

    proxy_host = 'http://localhost:8001'
    source = 'api/v1/widget-lockers/%(widget_locker_uuid)s/widgets/'


class WidgetDetailProxyViewSet(WidgetProxyViewSet):
    """
    A Proxy ViewSet to fetch data from the Widgets Service
    while maintaining a session.

    Example:
        - `/runtimes/<r_id>/widgets/` should internally call
            `/widget-lockers/<wl_id>/widgets/` and start a session for the `Runtime`.
        - `/runtimes/<r_id>/widgets/<w_id>/` should internally call
            `/widgets/<w_id>/` and update the session for the `Runtime`.
    """
    proxy_host = 'http://localhost:8001'
    source = 'api/v1/widget-lockers/%(widget_locker_uuid)s/widgets/%(widget_uuid)s/'


class WidgetDetailActionProxyViewSet(WidgetProxyViewSet):
    """
    A Proxy ViewSet to fetch data from the Widgets Service
    while maintaining a session.

    Example:
        - `/runtimes/<r_id>/widgets/` should internally call
            `/widget-lockers/<wl_id>/widgets/` and start a session for the `Runtime`.
        - `/runtimes/<r_id>/widgets/<w_id>/` should internally call
            `/widgets/<w_id>/` and update the session for the `Runtime`.
    """
    proxy_host = 'http://localhost:8001'
    source = 'api/v1/widget-lockers/%(widget_locker_uuid)s/widgets/%(widget_uuid)s/%(action)s/'

    def create_response(self, response):
        response = super(WidgetDetailActionProxyViewSet, self).create_response(response)
        # session info will be saved in a format determined by the client
        # everything might not be recorded
        # self.update_session(self.widget_uuid, response.data)
        return response

    def create_error_response(self, body, status):
        response = super(WidgetDetailActionProxyViewSet, self).create_error_response(body, status)
        # session info will be saved in a format determined by the client
        # everything might not be recorded
        # self.update_session(self.widget_uuid, response.data)
        return response

    def get_headers(self, request):
        # django.core.handlers.wsgi.WSGIRequest
        req = getattr(request, '_request')
        auth_header = req.META.get('HTTP_AUTHORIZATION')

        headers = super(WidgetDetailActionProxyViewSet, self).get_headers(request)
        if auth_header:
            # FIXME:
            # obtain the authorization from the widget schema :)
            headers['AUTHORIZATION'] = auth_header

        return headers
