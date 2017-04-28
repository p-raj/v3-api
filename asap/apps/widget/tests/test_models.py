#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# 3rd party
import uuid

# Django
from django.core.exceptions import ValidationError

# DRF
from rest_framework.test import RequestsClient

# own app
from asap.apps.widget.tests import base

client = RequestsClient()


class WidgetModelTestCase(base.WidgetTestCase):
    """includes test cases @ model level

    """

    def test_add_widget_object(self):
        """validate creation of Widget object @ model level, no naughty strings are allowed.

        """
        response = {}
        print(" validation start for bad_strings_clean_list")
        response['clean_list_validation results'] = []
        response['reject_list_validation results'] = []

        for string in self.bad_strings_clean_list:
            widget = self.model(name=string, process_locker_token=uuid.uuid4(), schema=dict())
            try:
                widget.clean()
            except ValidationError as e:
                pass

        print(" validation start for bad_strings_reject_list")

        for string in self.bad_strings_reject_list:
            widget = self.model(name=string, process_locker_token=uuid.uuid4(), schema=dict())
            try:
                widget.clean()
                response['reject_list_validation results'].append(string)
            except ValidationError as e:
                pass

        if response:
            d = {'reject_list_validation results': [], 'clean_list_validation results': []}
            self.assertDictEqual(response, d, response)

    def test_delete_widget_object(self):
        """validate deletion of Widget object @ model level.

        """
        self.assertRaisesMessage(ValidationError, self.widget_obj.delete())
