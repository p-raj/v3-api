import logging

from rest_framework.permissions import AllowAny
from rest_framework_proxy.views import ProxyView

from asap.apps.runtime.models.runtime import Runtime
from asap.apps.runtime.models.session import Session

logger = logging.getLogger(__name__)


class SessionMixin(ProxyView):
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

    def __init__(self):
        super(WidgetProxyViewSet, self).__init__()
        self.runtime_uuid = None
        self.widget_uuid = None

    def get_source_path(self):
        runtime = Runtime.objects.filter(uuid=self.kwargs.get('uuid')).first()
        if not runtime or not runtime.widget_locker_uuid:
            return None

        # get source path maps the kwargs to the path
        # let's add widget_locker_uuid to it
        self.kwargs.update(widget_locker_uuid=runtime.widget_locker_uuid)
        return super(WidgetProxyViewSet, self).get_source_path()

    def create_response(self, response):
        _response = response
        response = super(WidgetProxyViewSet, self).create_response(response)

        if response.status_code >= 400:
            try:
                response.data = _response.json()
            except Exception as e:
                # let's log to check when it fails
                logger.warning(e)

        # payload gets overridden anyways in logger._log_db_entry
        # so why bother sending it ?
        # remove the parameter from the method signature
        response['X-VRT-SESSION'] = self.get_session_uuid()
        return response

    def create_error_response(self, body, status):
        response = super(WidgetProxyViewSet, self).create_error_response(body, status)

        # payload gets overridden anyways in logger._log_db_entry
        # so why bother sending it ?
        # remove the parameter from the method signature
        response['X-VRT-SESSION'] = self.get_session_uuid()
        return response

    def proxy(self, request, *args, **kwargs):
        self.runtime_uuid = kwargs.get('uuid')
        self.widget_uuid = kwargs.get('widget_uuid')

        # fake API call to generate a session
        # if it doesn't exists :/
        self.get_session()

        return super(WidgetProxyViewSet, self).proxy(request, *args, **kwargs)


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
    proxy_host = 'http://172.18.0.1:8000'
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

        if req.META.get('HTTP_X_VRT_SESSION'):
            headers['X-VRT-SESSION'] = req.META.get('HTTP_X_VRT_SESSION')

        return headers
