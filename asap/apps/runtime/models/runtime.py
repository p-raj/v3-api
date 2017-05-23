#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property

from asap.apps.runtime.workflow import RuntimeWorkflowBuilder
from asap.core.models import Authorable, Humanizable, Publishable, \
    Timestampable, UniversallyIdentifiable
from asap.core.workflow import MistralWorkflow

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

    # the workflow to start when the runtime is invoked
    # each instance will have runtime execution / workflow execution
    workflow_uuid = models.CharField(max_length=512, null=True, blank=True)

    # the base workflow generated for each runtime
    # the workflow will be editable as JSON,
    # till we get a builder (~yahoo pipes)
    workflow = JSONField(null=True, blank=True)

    def __str__(self):
        return '{0}'.format(self.uuid)

    @cached_property
    def workflow_builder(self):
        return MistralWorkflow(RuntimeWorkflowBuilder(self))

    @property
    def workflow_name(self):
        return self.workflow_builder.builder.get_workflow_name()

    @property
    def workflow_json(self):
        return self.workflow_builder.dict()


@admin.register(Runtime)
class RuntimeAdmin(admin.ModelAdmin):
    raw_id_fields = ['author']
    list_display = ('id', 'name', 'uuid',
                    'widget_locker_uuid',)
