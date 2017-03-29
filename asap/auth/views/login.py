import logging

import requests
from django.conf import settings
from rest_framework import response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from asap.auth.serializers import LoginSerializer

VERIS_CLIENT_ID = getattr(settings, 'VERIS_CLIENT_ID', None)
VERIS_CLIENT_SECRET = getattr(settings, 'VERIS_CLIENT_SECRET', None)

logger = logging.getLogger(__name__)

if not VERIS_CLIENT_ID:
    logger.warning('VERIS_CLIENT_ID setting not available')
if not VERIS_CLIENT_SECRET:
    logger.warning('VERIS_CLIENT_SECRET setting not available')


class LoginView(GenericAPIView):
    """
    We'll keep the LoginView simple for now.
    """
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        enable post request for this view

        :param request:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.perform_action(serializer)

    def perform_action(self, serializer):
        """
        perform the action (login) once the data has been validated

        :param serializer:
        :return:
        """
        data = serializer.data
        data.update(**{
            'grant_type': 'password',
            'client_id': VERIS_CLIENT_ID,
            'client_secret': VERIS_CLIENT_SECRET
        })
        resp = requests.post(self._token_url(), data=data)
        return response.Response(data=resp.json(), status=resp.status_code)

    def _token_url(self):
        # get an access token from the authorization server
        wsgi_request = getattr(self.request, '_request')
        return '{scheme}://{host}{path}'.format(
            scheme='https' if wsgi_request.is_secure() else 'http',
            host=wsgi_request.get_host(),
            path='/oauth/token/'
        )
