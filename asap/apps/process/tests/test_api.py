#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# 3rd party
import uuid, requests
import ujson as json

# Django
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ValidationError

# DRF
from rest_framework.test import RequestsClient

# own app
from asap.apps.process import models



client = RequestsClient()


class ProcessTestCase(TestCase):
    """

    """
    model = models.Process
    bad_strings_clean_list = None
    bad_strings_reject_list = None


    # def setUp(self):
    #     self.model.objects.create(name="lion", resource_token=uuid.uuid4(), operation="no_op")

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

    def test_add_process_object(self):
        """
        """
        name = self.bad_strings_clean_list[14]
        operation = self.bad_strings_reject_list[20]
        process = self.model(name=name, resource_token=uuid.uuid4(), operation=operation)

        self.assertRaises(ValidationError, process.clean())


    # def test_proces_objcet_api(self):
    #     """
    #     :return:
    #     """
    #     upstream_url = getattr(settings, 'PROCESS_MICRO_SERVICE', 'http://localhost:8000')
    #     process = self.model.objects.get(name='lion')
    #     router = reverse('micro_service_v1:process-resolve', args=[str(process.token), ] )
    #     url = '{0}{1}'.format(upstream_url, router)
    #     response = client.get(url)
    #     assert response.status_code == 200
