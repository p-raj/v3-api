#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Widget
------

It is one of the most critical layers,
responsible for mapping the UI components to the processes.

"""
import functools

from django.conf import settings
from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.urls.base import reverse
from django.utils.translation import ugettext_lazy as _

from asap.core.models import Authorable, Humanizable, Timestampable, \
    UniversallyIdentifiable, Publishable

User = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Widget(Authorable, Humanizable, Publishable, Timestampable,
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

    # the rules defined by the admin needs
    # to be translated to mistral workflows :)
    # for each rule there might be a mini workflow
    # eg.
    # on saving a member ---> send him a notification
    # P1: Search Member
    # P2: Save Member
    # P3: Send notification
    #  trigger: P2
    #  condition: member.email --> contains --> veris.in
    #  action: P3
    #
    # P2' (mistral): Wait for input
    #  1.a. change the process URL, kind of proxy?, preventing changes in schema
    #  1.b. generate the schema with a different P2 url ?
    #  2. forwards the data to P2
    #  3. Checks the rule on complete and starts P3
    rules = JSONField(
        _('Widget Rules'),
        null=True, blank=True
    )

    # first of all, find a fucking better name :)
    # auto generated when a rule is created
    # eg.
    # for each rule:
    # P1 ----> condition ----> P2
    # P1 ----> P1'
    # where P1' is the temporary URL created
    # where the data will be stored per __session/execution__
    # process mappings ?
    # FIXME
    # move this to session ?
    # UPDATE: every process is a proxy
    # process_proxies = JSONField(
    #     _('Process Proxy'),
    #     null=True, blank=True
    # )

    # generate the workflow YAML and insert into mistral :)
    # workflow_json = JSONField(
    #     _('Workflow'),
    #     null=True, blank=True
    # )

    # the workflow to start when the widget is invoked
    # each instance will have widget execution / workflow execution
    workflow_uuid = models.CharField(max_length=512, null=True, blank=True)

    # the template consists of the layout of components
    # & their bindings to processes
    # we may have bindings that are
    # not associated with any processes
    template = JSONField(
        _('Widget Template'),
        null=True, blank=True,
        help_text=_('Widget Template, the list of components with their layout & styles'),
    )

    def __str__(self):
        return '{0}'.format(self.name)

    def get_process_rules(self, process_id):
        if not self.rules:
            return []

        assert type(self.rules) == list, \
            'rules need to an array, each rule should have ' \
            '- trigger, ' \
            '- action, ' \
            '- list of conditions'
        return [
            '{process_name} : {rule}'.format(**{
                'process_name': 'process_{0}'.format(_.get('action')[:6]),
                'rule': '<% {0} %>'.format(
                    functools.reduce(
                        lambda c1, c2: '{0} and {1}'.format(c1, c2),
                        _.get('conditions')
                    )
                )
            }) for _ in self.rules if _.get('trigger') == process_id
        ]

    @staticmethod
    def get_process_id(process):
        return process.get('uuid')

    @property
    def workflow_name(self):
        return 'widget_{widget}'.format(widget=self.uuid)

    def workflow_task(self, process_id):
        from asap.apps.widget.views.process_service import KEYSTORE_SERVER
        task = {
            'workflow': 'process_reversed',
            'input': {
                'url': '{store}/<% $.session %>/get/'.format(
                    store=KEYSTORE_SERVER
                ),
                'process': 'http://172.20.0.1:8000' + reverse('widget-process-proxy', kwargs={
                    'uuid': self.uuid,
                    'process_uuid': process_id
                }),
                'headers': {
                    'Process': process_id,
                    'Content-Type': 'application/json'
                }
            },
            'publish': {
                process_id: '<% task(process_{process}).result %>'.format(
                    process=process_id[:6]
                )
            },
            'publish-on-error': {
                process_id: '<% task(process_{process}).result %>'.format(
                    process=process_id[:6]
                )
            }
        }

        rules = self.get_process_rules(process_id)
        if rules:
            task['on-success'] = rules
        return task

    @property
    def workflow_json(self):
        return {
            'version': '2.0',
            self.workflow_name: {
                'description': self.description or '',
                'type': 'direct',
                'input': [
                    'session'
                ],
                'tasks': {
                    # FIXME
                    'process_{process}'.format(process=_.get('uuid')[:6]):
                        self.workflow_task(self.get_process_id(_)) for _ in self.processes_json
                }
            }
        }

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
class WidgetAdmin(admin.ModelAdmin):
    raw_id_fields = ['author']
    list_display = ('name', 'uuid', 'process_locker_token',)
    list_display_links = ('name',)
