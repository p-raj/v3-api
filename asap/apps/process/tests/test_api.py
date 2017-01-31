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
from django.conf import settings

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
        upstream_url = getattr(settings, 'PROCESS_MICRO_SERVICE', 'http://localhost:8000')
        process = self.model.objects.get(name='lion')
        router = reverse('micro_service_v1:process-resolve', args=[str(process.token), ] )
        url = '{0}{1}'.format(upstream_url, router)
        response = client.get(url)
        assert response.status_code == 200
