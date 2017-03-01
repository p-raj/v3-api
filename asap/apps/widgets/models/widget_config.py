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
import uuid, bleach

# Django
from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError

# local
from asap.core.models import Authorable, Timestampable
from asap.apps.utils import validator

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

    data = JSONField(
        _('Widget Data'),
        null=True, blank=True,
        help_text=_('Widget Data, the data to be filled by admin, using admin widget designed by developer'),
    )
    template = JSONField(
        _('Widget Template'),
        null=True, blank=True,
        help_text=_('Widget Template, the list of components with their layout & styles'),
    )

    # Functions
    def __str__(self):
        return '{0}'.format(self.name)

    def clean(self):
        """Validate models field data or clean fields data so that no bad strings can cause any problem.
        """

        # reject any malicious input string
        bad_strings_json = validator._get_bad_strings_json().get('rejected_list')

        if self.name in bad_strings_json:
            raise ValidationError(_('malicious input string sent in name. {0}'.format(self.name)))

        # validate char fields data length
        if len(self.name) > 30:
            raise ValidationError({'name': _('Length of name cannot be greater then 30')})

        # clean or bleach fields data
        self.name = bleach.clean(self.name)

    def save(self, **kwargs):
        self.clean()
        return super(Widget, self).save(**kwargs)


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    raw_id_fields = ['author']
    list_display = ('name', 'token', 'process_locker_token',)
    list_display_links = ('name',)
