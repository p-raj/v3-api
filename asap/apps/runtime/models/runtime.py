#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests

from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from asap.core.models import Authorable, Humanizable, Timestampable, \
    UniversallyIdentifiable, Publishable

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

    @property
    def workflow_name(self):
        return 'runtime_{runtime}'.format(runtime=self.uuid)

    @property
    def widgets(self):
        # FIXME
        # noinspection PyPep8Naming
        WidgetLocker_URL = 'http://172.20.0.1:8000/api/v1/widget-lockers/{wl_uuid}/widgets/'
        response = requests.get(WidgetLocker_URL.format(wl_uuid=self.widget_locker_uuid))

        # move these lame tasks to some place else
        # and make these smart
        return response.json().get('results')

    @property
    def workflow_json(self):
        tasks = {
            self.widget_workflow_task_name(_):
                self.workflow_task(_) for _ in self.widgets
        }
        publish_tasks = {
            self.publish_widget_workflow_task_name(_):
                self.publish_workflow_task(_) for _ in self.widgets
        }

        tasks.update(**publish_tasks)
        tasks.update({
            'wait_for_widgets': {
                'requires': [self.publish_widget_workflow_task_name(_) for _ in self.widgets]
            }
        })
        return {
            'version': '2.0',
            self.workflow_name: {
                'description': self.description,
                'type': 'reverse',
                'input': [
                    'session'
                ],
                'tasks': tasks
            }
        }

    @staticmethod
    def workflow_task(widget):
        return {
            'workflow': Runtime.widget_workflow_name(widget),
            'input': {
                'session': '<% $.session %>'
            },
            'publish': {
                'result': '<% task({widget_workflow}).result %>'.format(
                    widget_workflow=Runtime.widget_workflow_task_name(widget)
                )
            },
            'publish-on-error': {
                'result': '<% task({widget_workflow}).result %>'.format(
                    widget_workflow=Runtime.widget_workflow_task_name(widget)
                )
            }
        }

    @staticmethod
    def publish_workflow_task(widget):
        from asap.apps.widget.views.process_service import KEYSTORE_SERVER
        return {
            'action': 'std.http',
            'input': {
                'method': 'post',
                'url': '{store}/<% $.session %>/set/'.format(
                    store=KEYSTORE_SERVER
                ),
                'body': '<% task({widget_workflow}).result %>'.format(
                    widget_workflow=Runtime.widget_workflow_task_name(widget)
                ),
                'headers': {
                    'Process': widget.get('uuid'),
                    'Content-Type': 'application/json'
                }
            },
            'requires': [Runtime.widget_workflow_task_name(widget)]
        }

    @staticmethod
    def get_widget_id(widget):
        return widget.get('uuid')[:6]

    @staticmethod
    def widget_workflow_name(widget):
        return 'widget_{widget}'.format(widget=widget.get('uuid'))

    @staticmethod
    def widget_workflow_task_name(widget):
        return 'wait_for_{widget_workflow}'.format(
            widget_workflow=Runtime.widget_workflow_name(widget)[:13]
        )

    @staticmethod
    def publish_widget_workflow_task_name(widget):
        return 'publish_{widget_workflow}'.format(
            widget_workflow=Runtime.widget_workflow_name(widget)[:13]
        )

    def __str__(self):
        return '{0}'.format(self.uuid)


@admin.register(Runtime)
class RuntimeAdmin(admin.ModelAdmin):
    raw_id_fields = ['author']
    list_display = ('id', 'name', 'uuid',
                    'widget_locker_uuid',)
