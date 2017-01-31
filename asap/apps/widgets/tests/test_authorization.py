#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# DRF
from rest_framework.test import RequestsClient

# own app
from asap.apps.widgets.tests import base

client = RequestsClient()


class WidgetAuthorizationTestCase(base.WidgetTestCase):
    """

    """

    def test_authorization(self):
        """validate authorization of any request trying to access any Widget, whether that request is allowed or not.

        """
        # TODO : Need to write test-cases whenever proper authorization will be implemented on Widget service.
        pass
