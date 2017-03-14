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
    """Resource Viewset, every resource http request handles by this class

    """
    # TODO : remove AllowAny permission with proper permission class
    permission_classes = (permissions.AllowAny, )
    actor = 'resource'

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
        serializer = serializers.EmailNotificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        notify_lib = notification.NotifyAllLib()
        notify_lib.send_notification(**serializer.data)

        return Response(status=status.HTTP_200_OK)

    def send_sms(self, request):
        """

        :param request:
        :return:
        """
        pass

    def send_push(self, request):
        """

        :param request:
        :return:
        """
        pass
