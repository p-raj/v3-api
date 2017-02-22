"""
TODO:

Replace the functionality of this file with Kong.
"""
import logging

from django.conf import settings

from rest_framework.permissions import AllowAny
from rest_framework_proxy.views import ProxyView

logger = logging.getLogger(__name__)


class ProxyViewSet(ProxyView):
    """
    A Proxy ViewSet to fetch data from the Widgets Service
    while maintaining a session.

    Example:
        - `/runtimes/<r_id>/widgets/` should internally call
            `/widget-lockers/<wl_id>/widgets/` and start a session for the `Runtime`.
        - `/runtimes/<r_id>/widgets/<w_id>/` should internally call
            `/widgets/<w_id>/` and update the session for the `Runtime`.
    """
    proxy_host = settings.SERVER_URL
    source = '%(url)s'
    permission_classes = (AllowAny,)

    def get_host(self):
        return self.request.get_host()

    def get_source_path(self):
        if self.get_host().startswith('localhost') or self.get_host().startswith('192.168'):
            return super(ProxyViewSet, self).get_source_path()

        # runtime = Runtime.objects.filter(uuid=self.kwargs.get('uuid')).first()
        # if not runtime or not runtime.widget_locker_uuid:
        #     return None
        #
        # # get source path maps the kwargs to the path
        # # let's add widget_locker_uuid to it
        # self.kwargs.update(widget_locker_uuid=runtime.widget_locker_uuid)
        return 'proxy/{0}'.format(super(ProxyViewSet, self).get_source_path())

    def get_proxy_host(self):
        # we need to change the proxy host a zillion times :/
        # this won't happen when we separate out servers :)
        if self.get_host().startswith('runtime'):
            return settings.WIDGETS_MICRO_SERVICE
        if self.get_host().startswith('widget'):
            return settings.PROCESS_MICRO_SERVICE
        if self.get_host().startswith('process'):
            return settings.RESOURCE_MICRO_SERVICE
        if self.get_host().startswith('resource'):
            return settings.SERVER_URL

        # shouldn't be called :/
        return super(ProxyViewSet, self).get_proxy_host()

    def get_headers(self, request):
        # django.core.handlers.wsgi.WSGIRequest
        req = getattr(request, '_request')
        auth_header = req.META.get('HTTP_AUTHORIZATION')

        headers = super(ProxyViewSet, self).get_headers(request)
        if auth_header:
            # FIXME:
            # obtain the authorization from the widget schema :)
            headers['AUTHORIZATION'] = auth_header

        return headers

    def proxy(self, request, *args, **kwargs):
        return super(ProxyViewSet, self).proxy(request, *args, **kwargs)
