#!/usr/bin/python
# -*- coding: utf-8 -*-

# future
from __future__ import unicode_literals

from django.conf.urls import include, url

# own app
from asap.apps.widgets.views import WidgetViewSet, WidgetLockerViewSet
from asap.apps.widgets.views.process_service import ProcessActionProxyViewSet
from asap.router import Router

from rest_framework_nested import routers

router = Router()
router.register('widget-lockers', WidgetLockerViewSet)
router.register('widgets', WidgetViewSet)

routes_widget = routers.NestedSimpleRouter(Router.shared_router, 'widget-lockers', lookup='widget_locker')
routes_widget.register('widgets', WidgetViewSet, base_name='widget-lockers')

UUID_REGEX = '[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}'

urlpatterns = [
    url('', include(routes_widget.urls)),

    url(r'widgets/(?P<uuid>{uuid})/(?P<process_uuid>{uuid})/$'.format(uuid=UUID_REGEX),
        ProcessActionProxyViewSet.as_view(), name='widget-process-proxy'),
]
