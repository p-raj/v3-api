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
from django.contrib.auth import get_user_model

# own app
from asap.apps.runtime import models

User = get_user_model()


class RuntimeTestCase(TransactionTestCase):
    """Base class of Widget Test Case, it includes all possible test cases on widgets.
       Inherit this file and override respective test case method.

    """
    model = models.runtime.Runtime
    locker = models.runtime_locker.RuntimeLocker
    session = models.session.Session
    bad_strings_clean_list = None
    bad_strings_reject_list = None
    vrt_obj = None
    user = None

    def setUp(self):
        """

        """
        self.user = User.objects.create(username="lion")
        self.vrt_obj = self.model.objects.create(widget_locker_uuid=uuid.uuid4(), author=self.user)

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
        return getattr(settings, 'VRT_MICRO_SERVICE', 'http://172.20.0.1:8000')
