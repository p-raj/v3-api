#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- widgets.models.widget
~~~~~~~~~~~~~~

- This file contains the Widget service models that will map into DB tables and will store Widget data
  and Schema of Widget-Process relations, Rest Client
 """

# future
from __future__ import unicode_literals

# 3rd party
import uuid

# Django
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

# local
from asap.core.models import Authorable, Timestampable

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Widget(Authorable, Timestampable, models.Model):
    """Widgets are the collection of different Process & Rules.
       Process can be called based on some rules.Widget consists of a predefined Workflow.

    """

    # Attributes
    name = models.CharField(
            _('Widget Name'),
            max_length=30,
            help_text=_('Required. 30 characters or fewer.'),
    )
    token = models.UUIDField(
            _('Widget token'),
            default=uuid.uuid4,
            help_text=_('Widget token, widget is accessed via this token'),
    )
    process_locker_token = models.UUIDField(
                        _('Process Locker Token'),
                        help_text=_('Token of Process Locker to which will be loaded when a Widget is called.')
    )
    schema = JSONField(
             _('Widget Schema'),
             null=True, blank=True,
             help_text=_('Rules config, tells us which widget will be called based on what rules.'),
    )

    # Functions
    def __str__(self):
        return '{0}'.format(self.token)


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    raw_id_fields = ['author']
    list_display = ('name', 'token', 'process_locker_token', )
    list_display_links = ('name', )
