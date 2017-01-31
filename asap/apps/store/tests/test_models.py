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
from asap.apps.store.tests import base

client = RequestsClient()


class ResourceModelTestCase(base.ResourceTestCase):
    """

    """

    def setUp(self):
        self.resource_obj = self.model.objects.create(name="lion", upstream_url='http:0.0.0.0:8000', schema=dict())
        super(ResourceModelTestCase, self).setUp()

    def test_for_naughty_strings(self):
        """validate creation of resource object @ model level, no naughty strings are allowed.

        """
        response = {}
        print(" validation start for bad_strings_clean_list")
        response['clean_list_validation results'] = []
        response['reject_list_validation results'] = []

        for string in self.bad_strings_clean_list:
            name, operation = string, string
            resource = self.model(name=name,  upstream_url='http://0.0.0.0:8000', schema=dict())
            try:
                resource.clean()
            except ValidationError as e:
                pass

        print(" validation start for bad_strings_reject_list")

        for string in self.bad_strings_reject_list:
            name, operation = string, string
            resource = self.model(name=name,  upstream_url='http://0.0.0.0:8000', schema=dict())
            try:
                resource.clean()
                response['reject_list_validation results'].append(string)
            except ValidationError as e:
                pass

        if response:
            d = {'reject_list_validation results': [], 'clean_list_validation results': []}
            self.assertDictEqual(response, d, response)

    def test_delete_resource_object(self):
        """validate deletion of process object @ model level, no naughty strings are allowed.

        """
        self.assertRaisesMessage(ValidationError, self.resource_obj.delete())
