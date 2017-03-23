#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- micro_service.notification.router
~~~~~~~~~~~~~~~~~

- This file contains Notification service routers.
"""

# future
from __future__ import unicode_literals

# Django
from django.conf.urls import url

# own app
from asap.micro_services.notification import views


email_notification = views.NotificationViewSet.as_view({
    'post': 'send_email',
})

sms_notification = views.NotificationViewSet.as_view({
    'post': 'send_sms',
})

push_notification = views.NotificationViewSet.as_view({
    'post': 'send_push',
})

urlpatterns = [
        url(r'^email/$',
            email_notification,
            name='email-notification'),
        url(r'^sms/$',
            sms_notification,
            name='sms-notification'),
        url(r'^push/$',
            push_notification,
            name='push-notification'),
]
