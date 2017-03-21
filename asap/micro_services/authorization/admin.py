#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- micro_service.authorization.admin
~~~~~~~~~~~~~~

- This file contains admin models of authorization micro service
"""

# future
from __future__ import unicode_literals

# 3rd party


# Django
from django.contrib import admin


# local


# own app
from asap.micro_services.authorization import models


class AuthorizationAdmin(admin.ModelAdmin):
    """
    """
    list_display = ('id', 'token', 'source', 'target', 'create', 'update', 'read', 'delete', )
    list_display_links = ('token', 'source', 'target',)
    list_filter = ('create', 'update', 'read', 'delete', )
    search_fields = ('id', 'token', 'source', 'target', )
    list_per_page = 20
    ordering = ('-id',)

admin.site.register(models.Authorization, AuthorizationAdmin)


