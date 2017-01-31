#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# 3rd party
import uuid

# DRF
from rest_framework.test import RequestsClient

# own app
from asap.apps.process.tests import base

client = RequestsClient()


class ProcessAuthorizationTestCase(base.ProcessTestCase):
    """

    """

    def test_authorization(self):
        """validate authorization of any request trying to access any Process, whether that request is allowed or not.

        """
        # TODO : Need to write test-cases whenever proper authorization will be implemented on Process service.
        pass
