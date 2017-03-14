#!/usr/bin/python
# -*- coding: utf-8 -*-

# future
from __future__ import unicode_literals

# Django
from django.conf.urls import url, include

# local apps
from asap.micro_services.notification import router as notification_router

urlpatterns = [
    url(r'^notification/', include(notification_router)),

]
