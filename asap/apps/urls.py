#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import include, url

from asap.apps.process import routers as r_process
from asap.apps.runtime import routers as r_runtime
from asap.apps.widget import routers as r_widgets

urlpatterns = [
    url(r'', include(r_process)),
    url(r'', include(r_runtime)),
    url(r'', include(r_widgets)),
]
