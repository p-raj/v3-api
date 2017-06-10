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
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from reversion.admin import VersionAdmin

from asap.apps.process.models.process import Process
from asap.core.models import Authorable, Humanizable, Publishable, \
    Timestampable, UniversallyIdentifiable

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Widget(Authorable, Humanizable, Publishable, Timestampable,
             UniversallyIdentifiable, models.Model):
    """
    Widgets are the collection of different Process & Rules.
    Process can be called based on some rules.
    Widget consists of a predefined Workflow.
    """
    # we need to have a secure token
    # to access the process service, currently its more of a hack
    # and needs to be automated using a OAuth flow
    # process locker uuid may be shared by different widgets
    # process locker token is required for executing a process
    process_locker_uuid = models.CharField(max_length=512, null=True, blank=True)
    process_locker_token = models.CharField(
        _('Process Locker Token'), max_length=512,
        null=True, blank=True,
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

    processes = models.ManyToManyField(
        Process, related_name='widget_%(app_label)s_%(class)s', blank=True
    )

    # FIXME
    # temp hack
    # move to the through relation
    # between app/runtime/screen & widgets
    index = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return '{0}'.format(self.name)

    def has_permission(self, token):
        # TODO
        # whole thing doesn't feel right,
        # although it works :/
        import jwt
        from asap.apps.widget.models.widget_locker import WidgetLocker
        try:
            payload = WidgetLocker.decode(token)
        except jwt.DecodeError:
            return False
        return bool(self.widgetlocker_set.filter(uuid=payload.get('locker')).count())


@admin.register(Widget)
class WidgetAdmin(VersionAdmin):
    raw_id_fields = ['author']
    list_display = ('name', 'uuid', 'process_locker_token',)
    list_display_links = ('name',)
    search_fields = ('name', 'description', 'uuid')


@receiver(post_save, sender=Widget)
def temp_add_processes_using_process_locker(sender, **kwargs):
    if not kwargs.get('created'):
        return

    instance = kwargs.get('instance')
    instance.processes.add(*Process.objects.filter(processlocker__uuid=instance.process_locker_uuid))
