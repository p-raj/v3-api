#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# 3rd party
import uuid

# Django
from django.urls import reverse

# DRF
from rest_framework.test import RequestsClient

# own app
from asap.apps.widget.tests import base

client = RequestsClient()


class WidgetsAPITestCase(base.WidgetTestCase):
    """

    """

    def test_widget_objcet_api(self):
        """
        :return:
        """
        # test case for widget-detail (single object)

        router = reverse('widget-detail', args=[str(self.widget_obj.token), ])
        url = '{0}{1}'.format(self.upstream_url(), router)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        # test case for widget-list (multiple objects)

        router = reverse('widget-list')
        url = '{0}{1}'.format(self.upstream_url(), router)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_widget_locker_objcet_api(self):
        """
        :return:
        """
        locker = self.locker.objects.create(name='lion', token=uuid.uuid4(), rules=dict(), author=self.user)

        # test case for widgetlocker-detail (single object)

        router = reverse('widgetlocker-detail', args=[str(locker.token), ])
        url = '{0}{1}'.format(self.upstream_url(), router)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        # test case for widgetlocker-list (multiple objects)

        router = reverse('widgetlocker-list')
        url = '{0}{1}'.format(self.upstream_url(), router)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
