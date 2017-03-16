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
from asap.micro_services.notification import config


class EmailNotificationSerializer(serializers.Serializer):
    """Email Notification Serializer

    """
    to = serializers.EmailField(required=True)
    from_email = serializers.EmailField(required=False)
    subject = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    html_message = serializers.BooleanField(default=False)
    provider = serializers.ChoiceField(required=True, choices=config.EMAIL_NOTIFICATION_PROVIDER)
    notification_type = serializers.CharField(default=config.EMAIL)

    def validate_from_email(self, from_email):
        """
        :param from_email: from_email value send by client
        :return:
        """
        if not from_email:
            return config.DEFAULT_FROM_EMAIL
        return from_email


class SMSNotificationSerializer(serializers.Serializer):
    """SMS Notification Serializer

    """
    to = serializers.CharField(required=True)
    from_ = serializers.CharField(required=False)
    body = serializers.CharField(required=True)
    provider = serializers.ChoiceField(required=True, choices=config.SMS_NOTIFICATION_PROVIDER)
    notification_type = serializers.CharField(default=config.SMS)