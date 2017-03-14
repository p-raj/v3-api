#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- notification.serializers
~~~~~~~~~~~~~~

- This file contains the Notification (email, sms, push) Serializers.
 """

# future
from __future__ import unicode_literals

# DRF
from rest_framework import serializers

# local

# own app
from asap.micro_services import service_settings


class EmailNotificationSerializer(serializers.Serializer):
    """Email Notification Serializer

    """
    to = serializers.EmailField(required=True)
    from_email = serializers.EmailField(required=False)
    subject = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    html_message = serializers.BooleanField(default=False)
    provider = serializers.ChoiceField(required=True, choices=service_settings.EMAIL_NOTIFICATION_PROVIDER)
    notification_type = serializers.CharField(default=service_settings.EMAIL)

    def validate_from_email(self, from_email):
        """
        :param from_email: from_email value send by client
        :return:
        """
        if not from_email:
            return service_settings.DEFAULT_FROM_EMAIL
        return from_email
