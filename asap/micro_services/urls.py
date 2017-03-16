#!/usr/bin/python
# -*- coding: utf-8 -*-

# future
from __future__ import unicode_literals

# Django
from django.conf.urls import url, include

# local apps
from asap.micro_services.state_machine import router as states_router

urlpatterns = [
    url(r'^state/', include(states_router)),
]
