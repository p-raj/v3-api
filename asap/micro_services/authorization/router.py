#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- micro_service.authorization.router
~~~~~~~~~~~~~~~~~

- This file contains Authorization service routers.
"""

# future
from __future__ import unicode_literals

# Django
from django.conf.urls import url

# own app
from asap.micro_services.authorization import views


authorize = views.AuthorizationViewSet.as_view({
    'get': 'has_perm',
    'post': 'create_perm',
    'put': 'update_perm',
})


urlpatterns = [
        url(r'^$',
            authorize,
            name='authorization'),
]
