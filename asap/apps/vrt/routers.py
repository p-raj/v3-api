#!/usr/bin/python
# -*- coding: utf-8 -*-

# future
from __future__ import unicode_literals

# own app
from asap.apps.vrt.views import RuntimeViewSet, RuntimeLockerViewSet
from asap.apps.vrt.views.widget_service import WidgetListProxyViewSet, WidgetDetailProxyViewSet, \
    WidgetDetailActionProxyViewSet
from asap.router import Router

from django.conf.urls import include, url

from rest_framework_nested import routers

router = Router()
router.register('runtime-lockers', RuntimeLockerViewSet)
router.register('runtimes', RuntimeViewSet)

routes_runtime = routers.NestedSimpleRouter(Router.shared_router, 'runtime-lockers', lookup='runtime_locker')
routes_runtime.register('runtimes', RuntimeViewSet, base_name='runtime-lockers')

UUID_REGEX = '[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}'

urlpatterns = [
    url('', include(routes_runtime.urls)),

    url(r'runtimes/(?P<uuid>{uuid})/widgets/$'.format(uuid=UUID_REGEX),
        WidgetListProxyViewSet.as_view(), name='runtime-widget-proxy-list'),
    url(r'runtimes/(?P<uuid>{uuid})/widgets/(?P<widget_uuid>{uuid})/$'.format(uuid=UUID_REGEX),
        WidgetDetailProxyViewSet.as_view(), name='runtime-widget-proxy-detail'),
    url(r'runtimes/(?P<uuid>{uuid})/widgets/(?P<widget_uuid>{uuid})/(?P<action>.*)/$'.format(uuid=UUID_REGEX),
        WidgetDetailActionProxyViewSet.as_view(), name='runtime-widget-proxy-detail-action'),
]
