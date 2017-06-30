#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from rest_framework_nested import routers

from asap.apps.widget.views import WidgetLockerViewSet, WidgetViewSet
from asap.router import Router

router = Router()
router.register('widget-lockers', WidgetLockerViewSet)
router.register('widgets', WidgetViewSet)

routes_widget = routers.NestedSimpleRouter(Router.shared_router, 'widget-lockers', lookup='widget_locker')
routes_widget.register('widgets', WidgetViewSet, base_name='widget-lockers')

urlpatterns = [
    url('', include(routes_widget.urls)),
]
