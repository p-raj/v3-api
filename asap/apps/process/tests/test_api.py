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
from asap.apps.process.tests import base

client = RequestsClient()


class ProcessAPITestCase(base.ProcessTestCase):
    """

    """

    def setUp(self):
        self.model.objects.create(name="lion", resource_token=uuid.uuid4(), operation="no_op", endpoint_schema=dict())

    def test_proces_objcet_api(self):
        """
        :return:
        """
        process = self.model.objects.get(name='lion')

        # test case for process-detail (single object)

        router = reverse('process-detail', args=[str(process.token), ])
        url = '{0}{1}'.format(self.upstream_url(), router)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        # test case for process-list (multiple objects)

        router = reverse('process-list')
        url = '{0}{1}'.format(self.upstream_url(), router)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_proces_locker_objcet_api(self):
        """
        :return:
        """
        locker = self.locker.objects.create(name='lion', token=uuid.uuid4(), rules=dict())

        # test case for processlocker-detail (single object)

        router = reverse('processlocker-detail', args=[str(locker.token), ])
        url = '{0}{1}'.format(self.upstream_url(), router)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        # test case for processlocker-list (multiple objects)

        router = reverse('processlocker-list')
        url = '{0}{1}'.format(self.upstream_url(), router)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    # def test_proces_resolve_api(self):
    #     """
    #     """
    #     TODO : Need to write functional test cases for this.
    #     process = self.model.objects.get(name='lion')
    #     router = reverse('micro_service_v1:process-resolve', args=[str(process.token), ])
    #     url = '{0}{1}'.format(self.upstream_url(), router)
    #     response = client.post(url)
    #     self.assertEqual(response.status_code, 200)
