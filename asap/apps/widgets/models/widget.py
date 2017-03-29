#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Widget
------

It is one of the most critical layers,
responsible for mapping the UI components to the processes.

 """

from django.conf import settings
from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _

from asap.core.models import Authorable, Humanizable, Timestampable, UniversallyIdentifiable

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Widget(Authorable, Humanizable, Timestampable,
             UniversallyIdentifiable, models.Model):
    """
    Widgets are the collection of different Process & Rules.
    Process can be called based on some rules.
    Widget consists of a predefined Workflow.
    """

    # raw processes schema
    # we'll keep a the raw format provided by the process service
    # it will come in handy if the process schema changes
    # we'll have parsing according to process schema version
    # and widget schema can change version independent of the process schema
    processes_json = JSONField(null=True, blank=True)

    # we need to have a secure token
    # to access the process service, currently its more of a hack
    # and needs to be automated using a OAuth flow
    # process locker uuid may be shared by different widgets
    # process locker token is required for executing a process
    process_locker_uuid = models.CharField(max_length=512)
    process_locker_token = models.CharField(
        _('Process Locker Token'), max_length=512,
        help_text=_('Token of Process Locker '
                    'to which will be loaded when a Widget is called.')
    )

    # each process might need some additional
    # data to be passed along, the widget data contains
    # additional data per process
    # for instance the Auth header
    # for each service enabled (maybe)
    # this maybe abstracted out, if we try and
    # re-use the same widget with different data
    # for instance, an organization may buy
    # a service for its different departments
    data = JSONField(
        _('Widget Data'),
        null=True, blank=True,
        help_text=_('Widget Data, the data to be filled by admin, '
                    'using admin widget designed by developer'),
    )

    # the template consists of the layout of components
    # & their bindings to processes
    # we may have bindings that are
    # not associated with any processes
    template = JSONField(
        _('Widget Template'),
        null=True, blank=True,
        help_text=_('Widget Template, the list of components with their layout & styles'),
    )

    @property
    def schema(self):
        # TODO
        # generate schema from processes json
        return

    def __str__(self):
        return '{0}'.format(self.name)

    def has_permission(self, token):
        # TODO
        # whole thing doesn't feel right,
        # although it works :/
        import jwt
        from asap.apps.widgets.models.widget_locker import WidgetLocker
        try:
            payload = WidgetLocker.decode(token)
        except jwt.DecodeError:
            return False
        return bool(self.widgetlocker_set.filter(uuid=payload.get('locker')).count())


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    raw_id_fields = ['author']
    list_display = ('name', 'uuid', 'process_locker_token',)
    list_display_links = ('name',)
