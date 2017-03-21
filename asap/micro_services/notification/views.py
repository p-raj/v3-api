#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- notification.views
~~~~~~~~~~~~~~

- This file contains notification service actions like sed sms, email, push notifications.
"""

# future
from __future__ import unicode_literals

# 3rd party

# rest-framework
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

# local
from asap.micro_services.libs import notifyAll as notification

# own app
from asap.micro_services.notification import serializers


class NotificationViewSet(viewsets.GenericViewSet):
    """Notification Viewset, every notification http request handles by this class

    """
    # TODO : remove AllowAny permission with proper permission class
    permission_classes = (permissions.AllowAny, )

    def _validate(self, serializer, data):
        """

        :param serializer: serializer against which data to ve validated
        :param data: data to ve validated
        :return: validated data.
        """

        serializer_instance = serializer(data=data)
        serializer_instance.is_valid(raise_exception=True)
        return serializer_instance.data

    def send_email(self, request):
        """

        :param request:
        :return:

        POST Example :
        {
            "to": "example@gmail.com",
            "from_email":"admin@example.com",
            "subject": "micro service integration",
            "provider": "gmail",
            "body": "<h1>email Body comes here</h1>",
            "html_message":"true"
        }
        """
        data = self._validate(serializers.EmailNotificationSerializer, request.data)

        self.notify(data)
        return Response(status=status.HTTP_200_OK)

    def send_sms(self, request):
        """

        :param request:
        :return:

        POST EXAMPLE :
        {
            "to": "+9198********",
            "from_": "plivo",
            "provider": "plivo",
            "body": "micro service message"
        }
        """
        data = self._validate(serializers.SMSNotificationSerializer, request.data)

        self.notify(data)
        return Response(status=status.HTTP_200_OK)

    def send_push(self, request):
        """

        :param request:
        :return:
        """
        pass

    def notify(self, data):
        """

        :param data: Notification data
        """
        notify_lib = notification.NotifyAllLib()
        notify_lib.send_notification(**data)

