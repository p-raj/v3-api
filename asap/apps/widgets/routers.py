#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# local
from asap.router import Router

# own app
from asap.apps.widgets.views import widget_locker
#
router = Router()
router.register('widget-lockers', widget_locker.WidgetLockerViewSet)

urlpatterns = [
]

urlpatterns += router.urls
