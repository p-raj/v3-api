#!/usr/bin/python
# -*- coding: utf-8 -*-

# future
from __future__ import unicode_literals

from django.conf.urls import include, url

# own app
from asap.apps.organizations.views import MemberViewSet, OrganizationViewSet
from asap.router import Router

from rest_framework_nested import routers

router = Router()
router.register('organizations', OrganizationViewSet)
router.register('members', MemberViewSet, base_name='member')

routes_organization = routers.NestedSimpleRouter(Router.shared_router, 'organizations', lookup='organization')
routes_organization.register('members', MemberViewSet, base_name='organizations')

urlpatterns = [
    url('', include(routes_organization.urls))
]
