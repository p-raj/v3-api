#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.service_vault.models
~~~~~~~~~~~~~~

- This file contains the Service Vault models that will map into DB tables and Every micro-service will gets register here
 """

# future
from __future__ import unicode_literals

# 3rd party
from rest_framework.exceptions import ValidationError

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

# local
from asap.apps.libs import bravdo

# own app


class ServiceVault(models.Model):
    """Service Collection Model

    """

    # Attributes
    name = models.CharField(
            _('Service Name'),
            max_length=30,
            unique=True,  # because kong need unique names
            help_text=_('Required. 30 characters or fewer.'),
    )
    request_host = models.CharField(
            _('Request Host'),
            unique=True,  # because kong need unique request_path
            max_length=200,
            help_text=_('Resource Host, to be passed to kong')
    )
    upstream_url = models.URLField(
            _('upstream url of service.'),
            max_length=200,
            help_text=_('Required. 200 characters or fewer.'),
    )
    swagger_schema = JSONField(
            _('Swagger Client')
    )
    is_public = models.BooleanField(
            _('Make Service Public'),
            default=False,
            help_text=_('If checked , this service will be publicly available for use.'),
    )
    created_at = models.DateTimeField(
             _('created at'),
             auto_now_add=True,
             db_index=True,
             editable=False,
    )
    modified_at = models.DateTimeField(
             _('modified at'),
             auto_now_add=True,
             db_index=True,
             editable=False,
    )

    # Meta
    class Meta:
        verbose_name = _("Service Vault")
        verbose_name_plural = _("Services Vault")
        ordering = ["-created_at"]

    # Functions
    def __str__(self):
        return "Service {0}".format(self.name)

    def get_operations(self):
        """

        :return: swagger client operations
        """
        bravdo_client = bravdo.BravadoLib()

        try:
            swagger_spec = bravdo_client.get_client_from_spec(self.upstream_url, self.swagger_schema)
            return bravdo_client.get_all_operations(swagger_spec)
        except Exception as e:
            raise ValidationError({'detail': 'issues in reading swagger client, make sure swagger client you have uploaded is valid.'})
