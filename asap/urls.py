#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Veris URL Configuration

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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework.documentation import include_docs_urls
from rest_framework_nested import routers
from rest_framework_swagger.views import get_swagger_view

from asap.apps.process.views import ProcessLockerViewSet, ProcessViewSet
from asap.apps.runtime.views import RuntimeLockerViewSet, RuntimeViewSet, SessionViewSet
from asap.apps.runtime.views.widget_service import WidgetListProxyViewSet, WidgetDetailProxyViewSet, \
    WidgetDetailActionProxyViewSet
from asap.apps.widget.views import WidgetViewSet, WidgetLockerViewSet
from asap.apps.widget.views.process_service import ProcessActionProxyViewSet
from asap.core.views.revision import RevisionViewSet
from asap.core.views.version import VersionViewSet

from .router import Router

# all the routes in one place make the file big
# ideally the routes should be registered auto-magically,
# or where the view(set) is being created
# See: http://stackoverflow.com/a/22684199/1796173
# Credits: @ND
# The DRF docs introduced in 3.6
# http://www.django-rest-framework.org/topics/3.6-announcement/
# doesn't work properly with this approach :(
routes = Router()
routes.register('version', VersionViewSet)
routes.register('revision', RevisionViewSet)

routes.register('runtimes', RuntimeViewSet)
routes.register('sessions', SessionViewSet)
routes.register('widgets', WidgetViewSet)
routes.register('processes', ProcessViewSet)

routes_runtime = routers.NestedSimpleRouter(routes, 'runtimes', lookup='runtime')
routes_runtime.register('sessions', SessionViewSet)

# TODO
# remove
routes.register('process-lockers', ProcessLockerViewSet)
routes_process = routers.NestedSimpleRouter(routes, 'process-lockers', lookup='process_locker')
routes_process.register('processes', ProcessViewSet)
routes.register('widget-lockers', WidgetLockerViewSet)
routes_widget = routers.NestedSimpleRouter(routes, 'widget-lockers', lookup='widget_locker')
routes_widget.register('widgets', WidgetViewSet)
routes.register('runtime-lockers', RuntimeLockerViewSet)
routes_runtime_locker = routers.NestedSimpleRouter(routes, 'runtime-lockers', lookup='runtime_locker')
routes_runtime_locker.register('runtimes', RuntimeViewSet)

API_TITLE = 'Veris API'
UUID_REGEX = '[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}'

urlpatterns = [
    url(r'^schema/$', get_swagger_view(title=API_TITLE)),
    url(r'^docs/', include_docs_urls(title=API_TITLE, description='')),

    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^api/v1/', include(routes.urls)),

    # TODO
    # remove
    url(r'^api/v1/', include(routes_runtime.urls)),
    url(r'^api/v1/', include(routes_runtime_locker.urls)),
    url(r'^api/v1/', include(routes_widget.urls)),
    url(r'^api/v1/', include(routes_process.urls)),
    url(r'api/v1/runtimes/(?P<uuid>{uuid})/widgets/$'.format(uuid=UUID_REGEX),
        WidgetListProxyViewSet.as_view(), name='runtime-widget-proxy-list'),
    url(r'api/v1/runtimes/(?P<uuid>{uuid})/widgets/(?P<widget_uuid>{uuid})/$'.format(uuid=UUID_REGEX),
        WidgetDetailProxyViewSet.as_view(), name='runtime-widget-proxy-detail'),
    url(r'api/v1/runtimes/(?P<uuid>{uuid})/widgets/(?P<widget_uuid>{uuid})/(?P<action>.*)/$'.format(uuid=UUID_REGEX),
        WidgetDetailActionProxyViewSet.as_view(), name='runtime-widget-proxy-detail-action'),

    url(r'api/v1/widgets/(?P<uuid>{uuid})/(?P<process_uuid>{uuid})/$'.format(uuid=UUID_REGEX),
        ProcessActionProxyViewSet.as_view(), name='widget-process-proxy'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
