#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.db import models
from django.db.models import Case, When, Value
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
    list_display = ('id', 'name', 'uuid',)
    search_fields = ('name', 'description', 'uuid')
