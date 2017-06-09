#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.db import models
from django.db.models import Case, When, Value, Q
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _
from reversion.admin import VersionAdmin

from asap.apps.widget.models.widget import Widget
from asap.core.models import Authorable, Humanizable, Publishable, \
    Timestampable, UniversallyIdentifiable

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class RuntimeQueryset(models.QuerySet):
    def annotate_has_feedback(self, user):
        return self.annotate(
            has_feedback=Case(
                When(
                    feedback__isnull=False,
                    feedback__author=user,
                    then=Value(True)
                ),
                default=Value(False),
                output_field=models.BooleanField()
            )
        )


class Runtime(Authorable, Humanizable, Publishable, Timestampable,
              UniversallyIdentifiable, models.Model):
    # images are being stored on the media service
    # and only the URLs are saved here
    logo = models.URLField(blank=True)

    # TODO:
    # remove obsolete comments
    # the runtime service was built on Widget Service
    # it should provide widgets to the runtimes to which it has been associated
    # since the Widget service provides a way to group the widgets together,
    # so no need to maintain multiple widgets for a runtime here,
    # we'll keep a reference to the locker (group)
    # provided by the widget service instead
    widget_locker_uuid = models.CharField(max_length=64, null=True, blank=True)
    widget_locker_token = models.CharField(
        _('Widget Locker Token'), max_length=512,
        null=True, blank=True,
        help_text=_('Token of Widget Locker '
                    'to which will be loaded when a runtime is called.')
    )

    widgets = models.ManyToManyField(
        Widget, related_name='widget_%(app_label)s_%(class)s',
        blank=True
    )

    objects = RuntimeQueryset.as_manager()

    def __str__(self):
        return '{0}'.format(self.name)


@admin.register(Runtime)
class RuntimeAdmin(VersionAdmin):
    raw_id_fields = ['author']
    list_display = ('id', 'name', 'uuid',
                    'widget_locker_uuid',)
    search_fields = ('name', 'description', 'uuid')


@receiver(post_save, sender=Runtime)
def temp_add_widgets_using_widget_locker(sender, **kwargs):
    if not kwargs.get('created'):
        return

    instance = kwargs.get('instance')
    instance.widgets.add(*Widget.objects.filter(widgetlocker__uuid=instance.widget_locker_uuid))
