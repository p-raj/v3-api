#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
"""

# future
from __future__ import unicode_literals

# django
from django.contrib import admin

# own app
from asap.apps.process import models


class ProcessAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'resource_token', 'operation', )
    list_display_links = ('name', 'code', 'operation', )


class ProcessLockerAdmin(admin.ModelAdmin):
    list_display = ('name', 'token', 'is_publish', )
    list_display_links = ('name', 'token', )

admin.site.register(models.Process, ProcessAdmin)
admin.site.register(models.ProcessLocker, ProcessLockerAdmin)
