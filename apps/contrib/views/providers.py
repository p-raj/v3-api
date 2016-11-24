from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


class GithubAPIView(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
