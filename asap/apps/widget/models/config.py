#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.db import models
from reversion.admin import VersionAdmin

from asap.apps.process.models.process import Process
from asap.apps.widget.models.widget import Widget
from asap.core.models import Authorable, Timestampable


class ConfigManager(models.Manager):
    def get_by_natural_key(self, widget, process):
        return self.get(widget=widget, process=process)


class Config(Authorable, Timestampable, models.Model):
    objects = ConfigManager()

    process = models.ForeignKey(Process)
    widget = models.ForeignKey(Widget)

    config = JSONField(default={})
    transform = JSONField(default={})

    def natural_key(self):
        return self.widget, self.process

    natural_key.dependencies = [
        'widget.Widget',
        'process.Process'
    ]

    class Meta:
        unique_together = ('widget', 'process',)

    def __str__(self):
        return '{0}: {1}'.format(self.widget, self.process)


@admin.register(Config)
class ConfigAdmin(VersionAdmin):
    raw_id_fields = ('author', 'process', 'widget',)
    list_display = ('__str__', 'process', 'widget', 'created_at', 'modified_at')
    search_fields = ('process__name', 'widget__name', 'config',)

    def get_queryset(self, request):
        queryset = super(ConfigAdmin, self).get_queryset(request)
        return queryset.select_related('process', 'widget')
