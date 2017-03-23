#!/usr/bin/python
# -*- coding: utf-8 -*-

# future
from __future__ import unicode_literals

# Django
from django.conf.urls import url, include

# local apps
from asap.micro_services.notification import router as notification_router
from asap.micro_services.state_machine import router as states_router
from asap.micro_services.authorization import router as authorize_router

urlpatterns = [
    url(r'^notification/', include(notification_router)),
    url(r'^state/', include(states_router)),
    url(r'^authorize/', include(authorize_router)),
]
