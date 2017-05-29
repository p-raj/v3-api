#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from asap.core.models import Authorable, Humanizable, Publishable, \
    Timestampable, UniversallyIdentifiable

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Runtime(Authorable, Humanizable, Publishable, Timestampable,
              UniversallyIdentifiable, models.Model):
    # the runtime service was built on Widget Service
    # it should provide widgets to the runtimes to which it has been associated
    # since the Widget service provides a way to group the widgets together,
    # so no need to maintain multiple widgets for a runtime here,
    # we'll keep a reference to the locker (group)
    # provided by the widget service instead
    widget_locker_uuid = models.CharField(max_length=64, null=False, blank=False)
    widget_locker_token = models.CharField(
        _('Widget Locker Token'), max_length=512,
        help_text=_('Token of Widget Locker '
                    'to which will be loaded when a runtime is called.')
    )

    def __str__(self):
        return '{0}'.format(self.uuid)


@admin.register(Runtime)
class RuntimeAdmin(admin.ModelAdmin):
    raw_id_fields = ['author']
    list_display = ('id', 'name', 'uuid',
                    'widget_locker_uuid',)
