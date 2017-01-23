#!/usr/bin/python
# -*- coding: utf-8 -*-

# future
from __future__ import unicode_literals

from django.conf.urls import include, url

# own app
from asap.apps.widgets.views import WidgetViewSet, WidgetLockerViewSet
from asap.router import Router

from rest_framework_nested import routers

router = Router()
router.register('widget-lockers', WidgetLockerViewSet)
router.register('widgets', WidgetViewSet)

routes_widget = routers.NestedSimpleRouter(Router.shared_router, 'widget-lockers', lookup='widget_locker')
routes_widget.register('widgets', WidgetViewSet, base_name='widget-lockers')

urlpatterns = [
    url('', include(routes_widget.urls))
]
