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
from asap.apps.widget import schema
from asap.utils.models import Authorable, Humanizable, Publishable, \
    Timestampable, UniversallyIdentifiable

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class WidgetManager(models.Manager):
    def get_by_natural_key(self, uuid):
        return self.get(uuid=uuid)


class Widget(Authorable, Humanizable, Publishable, Timestampable,
             UniversallyIdentifiable, models.Model):
    """
    Widgets are the collection of different Process & Rules.
    Process can be called based on some rules.
    Widget consists of a predefined Workflow.
    """
    objects = WidgetManager()

    # TODO
    # deprecated
    # this used to come in handy for storing
    # the process config
    # it makes sense to store that config on an
    # object basis while adding relations
    data = JSONField(null=True, blank=True)

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

    process_configs = models.ManyToManyField(
        Process, blank=True,
        through='widget.Config'
    )

    # FIXME
    # temp hack
    # move to the through relation
    # between app/runtime/screen & widgets
    index = models.PositiveIntegerField(default=0, blank=True)

    def natural_key(self):
        return self.uuid,

    natural_key.dependencies = ['process.Process']

    @property
    def schema(self):
        return schema.generate(self)

    def __str__(self):
        return '{0}'.format(self.name)


@admin.register(Widget)
class WidgetAdmin(VersionAdmin):
    raw_id_fields = ['author']
    list_display = ('name', 'uuid',)
    list_display_links = ('name',)
    search_fields = ('name', 'description', 'uuid')


# FIXME
# hook for seamless transition
# to the new API :)
@receiver(post_save, sender=Widget)
def add_process_config(sender, **kwargs):
    instance = kwargs.get('instance')

    from asap.apps.widget.models.config import Config
    for key, value in (instance.data or {}).items():
        config, created = Config.objects.get_or_create(
            author=instance.author,
            widget=instance,
            process=Process.objects.get(uuid=key)
        )
        config.config = value
        config.save()
