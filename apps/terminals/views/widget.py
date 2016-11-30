import importlib

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK

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

    @detail_route(methods=['GET', 'POST'])
    def authenticate(self, request, pk=None):
        data = request.query_params.dict()
        from django.contrib.auth import authenticate
        user = authenticate(**data)

        if not user:
            return Response(status=HTTP_401_UNAUTHORIZED)

        if data.get('mfa') == 'true':
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
        data = request.query_params.dict()
        if data.get('otp') != '112233':
            return Response(status=HTTP_401_UNAUTHORIZED)

        from apps.contrib.serializers.users import UserSerializer
        serializer = UserSerializer(instance=request.user,
                                    context=self.get_serializer_context())
        return Response(serializer.data)
