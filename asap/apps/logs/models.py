#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- logs.models
~~~~~~~~~~~~~~

- This file contains Logging models of Veris Project.
"""

# future
from __future__ import unicode_literals

# Django
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib import admin


class ServiceLogs(models.Model):
    """
    All service logs will be manage here.
    """

    LOGGING_STATES = (
        ('init', 'Initialize'),
        ('in-progress', 'In Progress'),
        ('wait', 'Waiting'),
        ('handshake-initialize', 'Handshake Initiated'),
        ('handshake-succeed', 'Handshake Succeed'),
        ('handshake-failed', 'Handshake Failed'),
        ('succeeded', 'Completed'),
        ('failed', 'Failed'),
    )

    ACTOR_TYPES = (
        ('none', 'None'),
        ('vrt', 'Veris RunTime'),
        ('widget', 'Widget'),
        ('process', 'Process'),
        ('resource', 'Resource'),
    )

    # Attributes
    actor = models.CharField(
            _('Log belongs to'),
            max_length=10,
            default='none',
            choices=ACTOR_TYPES,
            help_text=_('Logs belongs to which actor'),
    )
    actor_token = models.UUIDField(
        _('Actor Token'),
        help_text=_('Actor token , so that we can identify an actor.'),
    )
    session = models.UUIDField(
        _('Log Session id'),
        help_text=_('Log session'),
    )
    handshake_token = models.UUIDField(
        _('Handshake Token'),
        blank=True,
        null=True,
        help_text=_('Token of actor/service to whom execution is handover by any current service.'),
    )
    handshake_status = models.BooleanField(
        _('Handshake Status'),
        default=False,
        help_text=_('Status of Handshake to whom execution is handover by any current service.'),
    )
    dataIn = JSONField(
        _('Request payload'),
        blank=True,
        null=True,
        help_text=_('Request payload, includes query_params, data etc.'),
    )
    dataOut = JSONField(
        _('Request response'),
        blank=True,
        null=True,
        help_text=_('Response that is returned via service.'),
    )
    state = models.CharField(
        _('current state of any request'),
        max_length=20,
        default='init',
        choices=LOGGING_STATES,
        help_text=_('Resource Request state at any given time.'),
    )
    status_code = models.PositiveIntegerField(
        _('Status code'),
        blank=True,
        null=True,
        help_text=_('Request status code sent in Response')
    )
    started_at = models.DateTimeField(
        _('Service execution start time.'),
        auto_now=False,
        db_index=True,
        help_text=_('When service initiated its task.'),
    )
    ended_at = models.DateTimeField(
        _('Service execution end time.'),
        auto_now=False,
        db_index=True,
        null=True,
        blank=True,
        help_text=_('When service completed its task.'),
    )

    # Meta
    class Meta:
        verbose_name = _("Service Logs")
        verbose_name_plural = _("Service Logs")
        ordering = ["-id"]
        get_latest_by = "id"

    # Functions
    def __str__(self):
        return "Service session Id{0}".format(self.session)

    # def clean(self):
    #     """Override clean() method to
    #         - check if status of log is 'fwd' then handshakeId must not be null
    #         - actor token is allowed null only if actor is resource, bec token can be found in payload
    #     """
    #     {'pub_date': _('Draft entries may not have a publication date.')}
    #     if not self.actor is 'resource' and self.actor_token is None:
    #         raise ValidationError({'actor_token': _('Actor Token cannot be null')})
    #
    #     if self.state in ('handshake-initialize', 'handshake-succeed', 'handshake-failed') and self.handshake_token is None:
    #         raise ValidationError({'handshake_token': _('Handshake Token cannot be null.')})


class ServiceLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'actor', 'actor_token', 'session', 'handshake_token', 'state', )
    list_display_links = ('actor', 'session',)

admin.site.register(ServiceLogs, ServiceLogAdmin)
