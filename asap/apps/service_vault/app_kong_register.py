#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.service-vault.app_kong_register
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- This file contains the function to register service-vault app in Kong
"""

# future
from __future__ import unicode_literals

# 3rd party


# Django
from django.conf import settings

# local
from asap.apps.libs import kong

# own app


APP_NAME = 'Service-Vault'
APP_REQUEST_HOST = 'vault.veris.in'
APP_UPSTREAM_URL = getattr(settings, 'VAULT_UPSTREAM_URL', None)


def add_service_vault_to_kong():
    """

    """
    return kong.add_api(
        APP_NAME,
        APP_REQUEST_HOST,
        APP_UPSTREAM_URL
    )
