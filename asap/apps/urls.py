#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# Django
from django.conf.urls import url, include
from django.conf import settings


urlpatterns = [
        
        url(r'', include('asap.apps.vrt.routers')),
        url(r'', include('asap.apps.widgets.routers')),
        url(r'', include('asap.apps.process_gw.routers')),
        url(r'', include('asap.apps.store.routers')),
]


