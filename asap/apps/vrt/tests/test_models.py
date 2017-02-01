#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# DRF
from rest_framework.test import RequestsClient

# own app
from asap.apps.vrt.tests import base

client = RequestsClient()


class RuntimeModelTestCase(base.RuntimeTestCase):
    """includes test cases @ model level

    """

    def test_runtime_object(self):
        """validate creation of Runtime object @ model level.

        """
        # create runtime object
        try:
            self.vrt_obj = self.model.objects.create(author=self.user, widget_locker_uuid='123456')
        except Exception as e:
            self.fail(e)

        # delete runtime object
        try:
            self.vrt_obj.delete()
        except Exception as e:
            self.fail(e)

    def test_locker_object(self):
        """validate creation of Runtime-Locker object @ model level.

        """
        # create locker object
        try:
            locker = self.locker.objects.create(author=self.user)
            locker.runtimes.add(self.vrt_obj)
        except Exception as e:
            self.fail(e)

        # Delete locker object

        try:
            locker.delete()
        except Exception as e:
            self.fail(e)

    def test_session_object(self):
        """validate creation of Runtime Session object @ model level.

        """
        # create session object
        try:
            session = self.session.objects.create(runtime=self.vrt_obj)
        except Exception as e:
            self.fail(e)

        # Delete session object

        try:
            session.delete()
        except Exception as e:
            self.fail(e)
