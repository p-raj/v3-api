from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

from django.http.response import HttpResponse

from rest_auth.registration.views import SocialLoginView


class GithubAPIView(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'http://192.168.1.96:8000/accounts/github/login/callback/'

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        response = HttpResponse('', status=302)
        response['Location'] = 'in.veris.terminal://veris?code={code}&state={state}' \
            .format(**request.query_params.dict())
        return response


class GoogleAPIView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'http://127.0.0.1:8000/accounts/google/login/callback/'
