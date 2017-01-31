#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# 3rd party
import ujson as json

# Django
from django.test import TransactionTestCase
from django.conf import settings

# own app
from asap.apps.store import models


class ResourceTestCase(TransactionTestCase):
    """Base class of Resource Test Case, it includes all possible test cases on resources.
       Inherit this file and override respective test case method.

    """
    model = models.Resource
    bad_strings_clean_list = None
    bad_strings_reject_list = None
    resource_obj = None

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
        return getattr(settings, 'RESOURCE_MICRO_SERVICE', 'http://localhost:8000')

