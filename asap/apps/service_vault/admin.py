#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
- apps.service_vault.admin
~~~~~~~~~~~~~~

- This file contains the admin models of Service Vault.
 """

# future
from __future__ import unicode_literals

# django
from django.contrib import admin

# own app
from asap.apps.service_vault import models


class ServiceVaultAdmin(admin.ModelAdmin):
    list_display = ('name', 'request_host', 'upstream_url', 'is_public', )
    list_display_links = ('name', 'request_host', 'upstream_url', )
    list_filter = ('is_public', )
    search_fields = ('name', 'request_host', 'upstream_url', )
    list_per_page = 20

admin.site.register(models.ServiceVault, ServiceVaultAdmin)
