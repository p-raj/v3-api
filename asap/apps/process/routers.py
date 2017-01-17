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

process_locker_resolve = views.ProcessLockerViewSet.as_view({
    'post': 'process_locker_resolve',
})

urlpatterns = [
        url(r'^process/(?P<token>[0-9a-z-]+)/$',
            process_locker_resolve,
            name='process-locker-resolve'),
]
