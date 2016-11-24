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
from apps.contrib.views import providers
from apps.contrib.views import UserViewSet
from apps.organizations.views import MemberViewSet, OrganizationViewSet

from django.conf import settings
from django.conf.urls import url, include

from django.contrib import admin

from rest_framework import routers

# let's keep a list of routes separate
# these route might reside on a remote server
remoteRouter = routers.DefaultRouter()
remoteRouter.register('users', UserViewSet)

router = routers.DefaultRouter()
router.register('members', MemberViewSet)
router.register('organizations', OrganizationViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api/v1/', include(remoteRouter.urls)),

    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^social/github/$', providers.GithubAPIView.as_view(), name='github_login')
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
