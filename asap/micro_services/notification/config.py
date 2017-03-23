#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- micro_services.notification.config
~~~~~~~~~~~~~~

- This file holds the general settings of notification micro-services.
 """

# django
from django.conf import settings

EMAIL = 'email'
SMS = 'sms'
PUSH = 'push'

EMAIL_NOTIFICATION_PROVIDER = ('gmail', )
SMS_NOTIFICATION_PROVIDER = ('plivo', )
PUSH_NOTIFICATION_PROVIDER = ('', )
NOTIFICATION_TYPES = (EMAIL, SMS, PUSH)

DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL', 'admin@example.com')