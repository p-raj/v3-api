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
from asap.apps.process.tests import base

client = RequestsClient()


class ProcessModelTestCase(base.ProcessTestCase):
    """includes test cases @ model level

    """

    def setUp(self):
        """

        """
        self.process_obj = self.model.objects.create(name="lion", resource_token=uuid.uuid4(), operation="no_op", endpoint_schema=dict())
        super(ProcessModelTestCase, self).setUp()

    def test_add_process_object(self):
        """validate creation of process object @ model level, no naughty strings are allowed.

        """
        response = {}
        print(" validation start for bad_strings_clean_list")
        response['clean_list_validation results'] = []
        response['reject_list_validation results'] = []

        for string in self.bad_strings_clean_list:
            name, operation = string, string
            process = self.model(name=name, resource_token=uuid.uuid4(), operation=operation)
            try:
                process.clean()
            except ValidationError as e:
                pass

        print(" validation start for bad_strings_reject_list")

        for string in self.bad_strings_reject_list:
            name, operation = string, string
            process = self.model(name=name, resource_token=uuid.uuid4(), operation=operation)
            try:
                process.clean()
                response['reject_list_validation results'].append(string)
            except ValidationError as e:
                pass

        if response:
            d = {'reject_list_validation results': [], 'clean_list_validation results': []}
            self.assertDictEqual(response, d, response)

    def test_delete_process_object(self):
        """validate deletion of process object @ model level, no naughty strings are allowed.

        """
        self.assertRaisesMessage(ValidationError, self.process_obj.delete())