#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# 3rd party
import ujson as json

# Django
from django.test import TestCase, TransactionTestCase
from django.conf import settings

# own app
from asap.apps.process import models


class ProcessTestCase(TransactionTestCase):
    """Base class of Process Test Case, it includes all possible test cases on process.
       Inherit this file and override respective test case method.

    """
    model = models.Process
    locker = models.ProcessLocker
    bad_strings_clean_list = None
    bad_strings_reject_list = None
    process_obj = None

    def setUp(self):
        """

        """
        self.bad_strings_clean_list = self._get_bad_strings_json().get('cleaned_list')
        self.bad_strings_reject_list = self._get_bad_strings_json().get('rejected_list')

    def _get_bad_strings_json(self):
        """

        :return: bad string json object.
        """
        json_data = open('static/bad_strings.json').read()
        return json.loads(json_data)

    def upstream_url(self):
        """
        """
        return getattr(settings, 'PROCESS_MICRO_SERVICE', 'http://localhost:8000')


    #
    # def test_add_process_object(self):
    #     """validate creation of process object @ model level, no naughty strings are allowed.
    #
    #     """
    #     pass
    #
    # def test_update_process_object(self):
    #     """validate updation of process object @ model level, no naughty strings are allowed and process token must not be changed.
    #
    #     """
    #     pass
    #
    # def test_delete_process_object(self):
    #     """validate deletion of process object @ model level, no naughty strings are allowed.
    #
    #     """
    #     pass
    #
    # def test_process_resolve_api(self):
    #     """validate process resolve API
    #
    #     """
    #     pass
    #
    # def test_object_level_api(self):
    #     """validate Process object level API.
    #
    #     """
    #     pass
    #
    # def test_authorization(self):
    #     """validate authorization of any request trying to access any Process, whether that request is allowed or not.
    #
    #     """
    #     pass
