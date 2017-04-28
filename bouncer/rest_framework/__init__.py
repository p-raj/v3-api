from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model


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
