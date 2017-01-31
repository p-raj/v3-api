#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# 3rd party
import ujson as json
import uuid
# Django
from django.test import TransactionTestCase
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
        self.process_obj = self.model.objects.create(name="lion", resource_token=uuid.uuid4(), operation="no_op", endpoint_schema=dict())

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

