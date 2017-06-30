#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from rest_framework_nested import routers

from asap.apps.runtime.views import RuntimeViewSet, SessionViewSet
from asap.apps.runtime.views.widget_process_execution import WidgetProcessExecution
from asap.apps.widget.views import WidgetViewSet
from asap.router import Router

router = Router()
router.register('runtimes', RuntimeViewSet)
router.register('sessions', SessionViewSet, base_name='runtimesession')

routes_runtime = routers.NestedSimpleRouter(Router.shared_router, 'runtimes', lookup='runtime')
routes_runtime.register('sessions', SessionViewSet, base_name='runtime-session')
routes_runtime.register('widgets', WidgetViewSet, base_name='runtime-widget')

urlpatterns = [
    url('', include(routes_runtime.urls)),

    url(r'widgets/(?P<widget_uuid>.*(?=/))/(?P<action>.*(?=/))/$',
        WidgetProcessExecution.as_view(), name='widget-action'),
    url(r'runtimes/(?P<uuid>.*(?=/))/widgets/(?P<widget_uuid>.*(?=/))/(?P<action>.*(?=/))/$',
        WidgetProcessExecution.as_view(), name='runtime-widget-action'),
]
