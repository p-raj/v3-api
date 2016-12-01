import importlib
import json

from allauth.socialaccount.models import SocialApp
from apps.contrib.serializers.social_app import SocialAppSerializer

from django.contrib.sites.models import Site

from apps.terminals.models.widget_container import WidgetContainer
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, \
    HTTP_405_METHOD_NOT_ALLOWED

from ..serializers.widget import Widget, WidgetAdminSerializer


def import_from_string(val):
    """
    Attempt to import a class from a string representation.
    """
    try:
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError('Could not import {}. {}: {}.'
                          .format(val, e.__class__.__name__, e))


class WidgetViewSet(viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetAdminSerializer

    @detail_route()
    def action(self, request, pk=None):
        # this route is just to make sure
        # we can distribute the application logic
        # in widget processes
        widget = self.get_object()
        config = json.loads(widget.config)
        action = request._request.path.split('/')[-2]

        if action not in config.get('private').get('actions'):
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

        return getattr(self, action)(request, pk)

    def _get_config(self, request, pk=None):
        if hasattr(self, '_widget_config'):
            return self._widget_config

        data = request.query_params.dict()
        # we'll get this from request somehow
        # asking this from params for now :(
        # TODO
        container = WidgetContainer.objects.get(pk=data.get('container'))
        self._widget_config = json.loads(container.config)
        return self._widget_config

    @detail_route(methods=['GET', 'POST'])
    def authenticate(self, request, pk=None):
        config = self._get_config(request, pk)

        if not bool(config.get('allow_form_login')):
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

        data = request.query_params.dict()
        from django.contrib.auth import authenticate
        user = authenticate(**data)

        if not user:
            return Response(status=HTTP_401_UNAUTHORIZED)

        if bool(config.get('is_mfa_enabled')):
            return Response(status=HTTP_200_OK, headers={
                'X-HTTP-MFA': 'totp',
                'X-MFA-TOKEN': 'mfa-token-of-user'
            })

        from apps.contrib.serializers.users import UserSerializer
        serializer = UserSerializer(instance=user,
                                    context=self.get_serializer_context())

        return Response(serializer.data)

    @detail_route(methods=['GET', 'POST'])
    def mfa(self, request, pk=None):
        config = self._get_config(request, pk)
        if not bool(config.get('is_mfa_enabled')):
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

        data = request.query_params.dict()
        if data.get('otp') != '112233':
            return Response(status=HTTP_401_UNAUTHORIZED)

        from apps.contrib.serializers.users import UserSerializer
        serializer = UserSerializer(instance=request.user,
                                    context=self.get_serializer_context())
        return Response(serializer.data)

    @detail_route(methods=['GET'])
    def providers(self, request, pk=None):
        config = self._get_config(request, pk)
        site = Site.objects.get_current(request)

        social_apps = SocialApp.objects.filter(
            sites=site,
            provider__in=config.get('providers')
        )
        serializer = SocialAppSerializer(instance=social_apps, many=True,
                                         context=self.get_serializer_context())
        return Response(serializer.data)
