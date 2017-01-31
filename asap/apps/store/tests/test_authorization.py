#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# DRF
from rest_framework.test import RequestsClient

# own app
from asap.apps.store.tests import base

client = RequestsClient()


class ResourceAuthorizationTestCase(base.ResourceTestCase):
    """

    """

    def setUp(self):
        self.model.objects.create(name="lion", upstream_url='http:0.0.0.0:8000', schema=dict())

    def test_authorization(self):
        """validate authorization of any request trying to access any Resource, whether that request is allowed or not.

        """
        # TODO : Need to write test-cases whenever proper authorization will be implemented on Resource service.
        pass
