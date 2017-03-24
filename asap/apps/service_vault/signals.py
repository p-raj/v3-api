#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.service-vault.signals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- This file contains the Service-Vault app signals
"""

# future
from __future__ import unicode_literals

# 3rd party

# Django
from django.db.models.signals import post_save
from django.dispatch import receiver

# local
from asap.apps.libs import kong

# own app
from asap.apps.service_vault.models import ServiceVault


@receiver(post_save, sender=ServiceVault)
def add_service_ob_to_kong(sender, instance, created=False, **kwargs):
    """

    :param sender: Signal sender
    :param instance: Service vault instance
    :param created: If new onj is created or updated
    :param kwargs: Signal kwargs
    """
    if created:
        kong.add_api(
            instance.name,
            instance.request_host,
            instance.upstream_url
        )

