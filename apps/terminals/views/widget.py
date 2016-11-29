from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK

from ..serializers.widget import Widget, WidgetSerializer


class WidgetViewSet(viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer

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
        serializer = UserSerializer(instance=user, context={
            'request': request
        })

        return Response(serializer.data)

    @detail_route(methods=['GET', 'POST'])
    def mfa(self, request, pk=None):
        data = request.query_params.dict()
        if data.get('otp') != '112233':
            return Response(status=HTTP_401_UNAUTHORIZED)

        from apps.contrib.serializers.users import UserSerializer
        serializer = UserSerializer(instance=request.user, context={
            'request': request
        })
        return Response(serializer.data)
