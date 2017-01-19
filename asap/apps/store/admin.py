#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# django
from django.contrib import admin

# own app
from asap.apps.store import models


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'upstream_url', 'token', )
    list_display_links = ('name', 'upstream_url', )

admin.site.register(models.Resource, ResourceAdmin)
