import uuid

from asap.apps.logs.logging import ServiceLogging

from rest_framework.permissions import AllowAny

from rest_framework_proxy.views import ProxyView


class LoggingProxyViewSet(ProxyView):
    permission_classes = (AllowAny,)

    logger = None
    session = uuid.uuid4()
    actor = 'vrt'

    def __init__(self, **kwargs):
        super(LoggingProxyViewSet, self).__init__(**kwargs)
        self.runtime_uuid = None
        self.widget_uuid = None

    def _init_logger_(self, request, token):
        """
        :param request : Django request object.
        :param token : widget token, helps in identifying the widget
        :return: logging class instance
        """
        self.logger = ServiceLogging(
            self.actor, token, self.session,
            payload=request.data or dict()
        )

    def create_response(self, response):
        self.logger.handshake_succeed(self.widget_uuid, None, response)
        response = super(LoggingProxyViewSet, self).create_response(response)

        # payload gets overridden anyways in logger._log_db_entry
        # so why bother sending it ?
        # remove the parameter from the method signature
        self.logger.success(response)  # logged as success
        return response

    def create_error_response(self, body, status):
        self.logger.handshake_failed(self.widget_uuid, None, status, body)
        response = super(LoggingProxyViewSet, self).create_error_response(body, status)

        # payload gets overridden anyways in logger._log_db_entry
        # so why bother sending it ?
        # remove the parameter from the method signature
        self.logger.fail(response)  # logged as failure
        return response

    def proxy(self, request, *args, **kwargs):
        self.runtime_uuid = kwargs.get('uuid')
        self.widget_uuid = kwargs.get('widget_uuid')

        if self.logger is None:
            self._init_logger_(request, self.runtime_uuid)

        self.logger.initialize()
        self.logger.handshake(self.widget_uuid, request.data)
        return super(LoggingProxyViewSet, self).proxy(request, *args, **kwargs)


class WidgetListProxyViewSet(LoggingProxyViewSet):
    """
    A Proxy ViewSet to fetch data from the Widgets Service
    while maintaining a session.

    Example:
        - `/runtimes/<r_id>/widgets/` should internally call
            `/widget-lockers/<wl_id>/widgets/` and start a session for the `Runtime`.
        - `/runtimes/<r_id>/widgets/<w_id>/` should internally call
            `/widgets/<w_id>/` and update the session for the `Runtime`.
    """
    proxy_host = 'http://localhost:8000'
    source = '/api/v1/widgets/'


class WidgetDetailProxyViewSet(LoggingProxyViewSet):
    """
    A Proxy ViewSet to fetch data from the Widgets Service
    while maintaining a session.

    Example:
        - `/runtimes/<r_id>/widgets/` should internally call
            `/widget-lockers/<wl_id>/widgets/` and start a session for the `Runtime`.
        - `/runtimes/<r_id>/widgets/<w_id>/` should internally call
            `/widgets/<w_id>/` and update the session for the `Runtime`.
    """
    proxy_host = 'http://localhost:8000'
    source = 'api/v1/widgets/%(widget_uuid)s'


class WidgetDetailActionProxyViewSet(LoggingProxyViewSet):
    """
    A Proxy ViewSet to fetch data from the Widgets Service
    while maintaining a session.

    Example:
        - `/runtimes/<r_id>/widgets/` should internally call
            `/widget-lockers/<wl_id>/widgets/` and start a session for the `Runtime`.
        - `/runtimes/<r_id>/widgets/<w_id>/` should internally call
            `/widgets/<w_id>/` and update the session for the `Runtime`.
    """
    proxy_host = 'http://localhost:8000'
    source = 'api/v1/widgets/%(widget_uuid)s/%(action)s/'
