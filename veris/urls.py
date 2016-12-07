"""veris URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from apps.libs.rest_auth import providers
from apps.libs.allauth import EmailAddressViewSet, SocialAppViewSet
from apps.libs.django import UserViewSet
from apps.organizations.views import MemberViewSet, OrganizationViewSet
from apps.terminals.views import ScreenViewSet, TerminalViewSet, \
    WidgetViewSet, WidgetContainerViewSet

from django.conf import settings
from django.conf.urls import url, include

from django.contrib import admin

# let's keep a list of routes separate
# these route might reside on a remote server

from .router import Router

urlpatterns = [
    url(r'^api/v1/', include(Router.shared_router.urls)),

    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/', include('allauth.urls')),

    # we have our own oauth provider
    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # we'll provide multi factor authentication
    url(r'', include('two_factor.urls', 'two_factor')),

    # {provider}_login name is used internally by django-allauth,
    # so let's use api_{provider}_login
    url(r'^social/github/$', providers.GithubAPIView.as_view(), name='api_github_login'),
    url(r'^social/google/$', providers.GoogleAPIView.as_view(), name='api_google_login')
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
