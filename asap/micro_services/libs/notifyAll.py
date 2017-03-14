#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- micro_services.libs.notifyAll
~~~~~~~~~~~~~~

-   This file contains the notifyAll third party library classes/functions which we are going to use in Notification.
    micro-service, so every request to third party will goes from here so in future if we replace any lib with another
    our core code will not be changed , we just needs to update this file.

-   Here we will create a proxy class for actual lib which will reverse proxy the request to that lib.
 """


# future
from __future__ import unicode_literals

# 3rd party libs
from notifyAll.services import notifier

# rest-framework
from rest_framework.exceptions import ValidationError

# local
from asap.micro_services import service_settings


class NotifyAllLib(object):
    """A Proxy class of notifyAll library

    ref : https://github.com/inforian/django-notifyAll
    """

    def _prepare_notification_message(self, *args, **kwargs):
        """

        :return: notification message as per notification_type
        """
        if kwargs.get('notification_type') == service_settings.EMAIL:
            return self._email_message(*args, **kwargs)
        elif kwargs.get('notification_type') == service_settings.SMS:
            return self._sms_message(*args, **kwargs)
        elif kwargs.get('notification_type') == service_settings.PUSH:
            return self._push_message(*args, **kwargs)
        else:
            raise ValidationError({'detail': 'Unknown notification service.'})

    def _email_message(self, *args, **kwargs):
        """

        :return:
        """
        context = {
            'subject': kwargs.get('subject', ''),
            'body': kwargs.get('body', ''),
            'html_message': kwargs.get('body', '') if kwargs.get('html_message') is True else None
        }

        return {
            'source': kwargs.get('from_email'),
            'destination': kwargs.get('to'),
            'notification_type': service_settings.EMAIL,
            'provider': kwargs.get('provider'),
            'context': context,
        }

    def _sms_message(self, *args, **kwargs):
        """

        :return:
        """
        return {
            'source': kwargs.get('from_'),
            'destination': kwargs.get('to'),
            'notification_type': service_settings.SMS,
            'provider': kwargs.get('provider'),
            'context': {
                'body': kwargs.get('body')
            },
        }

    def _push_message(self, *args, **kwargs):
        """

        :return:
        """
        pass

    def send_notification(self, *args, **kwargs):
        """

        :return: error if any otherwise send notification to respective destination
        """
        message = self._prepare_notification_message(*args, **kwargs)

        notification = notifier.Notifier(**message)

        try:
            notification.notify()
        except Exception as e:
            raise ValidationError(e)

