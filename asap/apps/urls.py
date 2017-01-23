#!/usr/bin/python
# -*- coding: utf-8 -*-

# future
from __future__ import unicode_literals

from asap.apps.authentication import urls as r_authentication
from asap.apps.organizations import routers as r_organizations

from asap.apps.process import routers as r_process
from asap.apps.store import routers as r_store
from asap.apps.vrt import routers as r_runtime
from asap.apps.widgets import routers as r_widgets

# Django
from django.conf.urls import url, include

urlpatterns = [
    url(r'', include(r_authentication)),
    url(r'', include(r_organizations)),

    url(r'', include(r_process)),
    url(r'', include(r_runtime)),
    url(r'', include(r_store)),
    url(r'', include(r_widgets)),
]
