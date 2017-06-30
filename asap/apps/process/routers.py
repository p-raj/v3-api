#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from rest_framework_nested import routers

from asap.apps.process.views import ProcessLockerViewSet, ProcessViewSet
from asap.router import Router

router = Router()
router.register('process-lockers', ProcessLockerViewSet)
router.register('processes', ProcessViewSet)

routes_process = routers.NestedSimpleRouter(Router.shared_router, 'process-lockers', lookup='process_locker')
routes_process.register('processes', ProcessViewSet, base_name='process-lockers')

urlpatterns = [
    url('', include(routes_process.urls))
]
