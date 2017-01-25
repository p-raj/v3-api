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


class ProcessAuthorizationTestCase(base.ProcessTestCase):
    """

    """

    def setUp(self):
        self.model.objects.create(name="lion", resource_token=uuid.uuid4(), operation="no_op")

    def test_authorization(self):
        """validate authorization of any request trying to access any Process, whether that request is allowed or not.

        """
        pass
