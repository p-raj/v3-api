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
from asap.apps.widget import models

User = get_user_model()


class WidgetTestCase(TransactionTestCase):
    """Base class of Widget Test Case, it includes all possible test cases on widgets.
       Inherit this file and override respective test case method.

    """
    model = models.widget.Widget
    locker = models.widget_locker.WidgetLocker
    bad_strings_clean_list = None
    bad_strings_reject_list = None
    widget_obj = None
    user = None

    def setUp(self):
        """

        """
        self.user = User.objects.create(username="lion")
        self.widget_obj = self.model.objects.create(name="lion", process_locker_token=uuid.uuid4(), schema=dict(), author=self.user)

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
        return getattr(settings, 'WIDGETS_MICRO_SERVICE', 'http://172.20.0.1:8000')
