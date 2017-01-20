#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- process.routers
~~~~~~~~~~~~~~~~~

- This file contains process routers.
"""

# future
from __future__ import unicode_literals

# Django
from django.conf.urls import url

# own app
from asap.apps.process import views


process_resolve = views.ProcessViewSet.as_view({
    'post': 'process_resolve',
})
process_locker_resolve = views.ProcessViewSet.as_view({
    'post': 'process_locker_resolve',
})

urlpatterns = [
        url(r'^process/(?P<token>[0-9a-z-]+)/$',
            process_resolve,
            name='process-resolve'),
        url(r'^process-locker/(?P<token>[0-9a-z-]+)/$',
            process_locker_resolve,
            name='process-locker-resolve'),
]

