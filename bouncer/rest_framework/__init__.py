import logging

import jwt
from box import Box
from django.conf import settings
from django.contrib.auth import get_user_model
from jwt.exceptions import DecodeError
from rest_framework.authentication import BaseAuthentication

logger = logging.getLogger(__name__)


class VerisAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        header = request.META.get('HTTP_VERIS_RESOURCE', '')

        # TODO
        # - validate the resource being sent
        splices = header.split()
        if not splices or splices[0].lower() != 'veris':
            return None

        # FIXME
        # - validate the resource being sent
        user, created = get_user_model().objects.get_or_create(username=splices[1])
        return user, user.username

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        # TODO
        # for better debugging
        return None


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return None

        try:
            data = Box(jwt.decode(
                token,
                secret=getattr(settings, 'JWT_SECRET'),
                aud=getattr(settings, 'AUDIENCE')
            ))
        except DecodeError as e:
            logger.debug('invalid token received: %s', e, exc_info=1)
            return None

        user, created = get_user_model().objects.get_or_create(username=data.user_info.uuid)
        if created:
            user.meta = data.user_info
            user.save()
        return user, token

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        # TODO
        # for better debugging
        return None
