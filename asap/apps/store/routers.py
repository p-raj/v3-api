#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- store.routers
~~~~~~~~~~~~~~~~~

- This file contains store routers.
"""

# future
from __future__ import unicode_literals

# Django
from django.conf.urls import url

# own app
from asap.apps.store import views


resource_resolve = views.ResourceViewSet.as_view({
    'post': 'resource_resolve',
})

urlpatterns = [
        url(r'^resource/(?P<token>[0-9a-z-]+)/(?P<operation_id>[-a-z-_]+)/$',
            resource_resolve,
            name='resource-resolve'),
]
