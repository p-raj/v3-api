#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- *apps.libs.kong
~~~~~~~~~~~~~~

- This file contains all the necessary function to interact with kong, any call made to kong from asap.apps will goes
    from here.

ref : https://getkong.org/docs/0.5.x/admin-api/

"""

# future
from __future__ import unicode_literals

# 3rd party
import requests
from rest_framework.exceptions import ValidationError

# Django
from django.conf import settings

# local


# own app


KONG_API_HOST = getattr(settings, 'KONG_API_HOST', None)


def add_api(name, request_host, upstream_url):
    """

    :param name: Name of API/Service
    :param request_host: request host for API
    :param upstream_url: upstream url for API
    :return: HTTP 201 with API dict
    """
    data = {
        'name': name,
        'request_host': request_host,
       # 'request_path': '/o',
        'upstream_url': upstream_url,
        'strip_request_path': True
    }
    add_api_url = '{0}{1}'.format(KONG_API_HOST, 'apis/')
    response = requests.post(add_api_url, data=data)

    if response.status_code is not 201:
        raise ValidationError(response.json())
    return response
