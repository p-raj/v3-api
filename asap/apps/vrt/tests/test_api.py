#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# 3rd party
import uuid

# Django
from django.urls import reverse

# DRF
from rest_framework.test import RequestsClient

# own app
from asap.apps.vrt.tests import base

client = RequestsClient()


class RuntimeAPITestCase(base.RuntimeTestCase):
    """

    """

    def test_vrt_objcet_api(self):
        """
        :return:
        """
        # test case for runtime-detail (single object)

        router = reverse('runtime-detail', args=[str(self.vrt_obj.uuid), ])
        url = '{0}{1}'.format(self.upstream_url(), router)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        # test case for runtime-list (multiple objects)

        router = reverse('runtime-list')
        url = '{0}{1}'.format(self.upstream_url(), router)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_vrt_locker_objcet_api(self):
        """
        :return:
        """
        locker = self.locker.objects.create(author=self.user)

        locker.runtimes.add(self.vrt_obj)

        # test case for runtimelocker-detail (single object)

        router = reverse('runtimelocker-detail', args=[str(locker.uuid), ])
        url = '{0}{1}'.format(self.upstream_url(), router)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        # test case for runtimelocker-list (multiple objects)

        router = reverse('runtimelocker-list')
        url = '{0}{1}'.format(self.upstream_url(), router)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_vrt_session_objcet_api(self):
        """
        :return:
        """
        # create session
        router = reverse('runtimesession-list')
        url = '{0}{1}'.format(self.upstream_url(), router)

        vrt_hyperlink = '{0}{1}'.format(self.upstream_url(), reverse('runtime-detail', args=[str(self.vrt_obj.uuid), ]))
        response = client.post(url, data={'runtime': vrt_hyperlink})
        self.assertEqual(response.status_code, 201)


        session = self.session.objects.create(runtime=self.vrt_obj)

        # test case for runtimesession-detail (single object)

        router = reverse('runtimesession-detail', args=[str(session.uuid), ])
        url = '{0}{1}'.format(self.upstream_url(), router)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

        # test case for runtimesession-list (multiple objects)

        router = reverse('runtimesession-list')
        url = '{0}{1}'.format(self.upstream_url(), router)
        response = client.get(url)
        self.assertEqual(response.status_code, 200)