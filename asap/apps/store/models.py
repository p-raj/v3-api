#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
-store.models
-~~~~~~~~~~~~~~


-This file contains the Resource models that will map into DB tables and will store data of Resources
 """

# future
from __future__ import unicode_literals

# django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField

# 3rd party
import uuid

RESOURCE_REQUEST_STATES = (
        ('init', 'Initialize'),
        ('inprocess', 'In Process'),
        ('wait', 'Waiting'),
        ('succeeded', 'Completed'),
        ('failed', 'Failed'),
    )

class Resource(models.Model):
    """
    Resource is any service which will be either Provided by Veris or any 3rd party.
    Resource cannot be called independently , to access any resource it must first bound with a process.

    Note:
        - name & upstream_url will be unique together so that no Admin can add two upstraem url with
          same name. Because that will be very confusing.
    """

    # Attributes
    name = models.CharField(
            _('resource name'),
            max_length=30,
            help_text=_('Required. 30 characters or fewer.'),
    )
    upstream_url = models.URLField(
                    _('upstream url of resource.'),
                    max_length=200,
                    help_text=_('Required. 200 characters or fewer.'),
    )
    schema = JSONField(
             _('Resource schema'),
             help_text=_('Resource swagger client schema.'),
    )
    token = models.UUIDField(
            _('Resource token'),
            unique=True,
            default=uuid.uuid4,
            editable=False,
            help_text = _('Non-editable, to be generated by system itself.This token to be bind with process\
             Process will access Resource with the help of this token'),
    )
    created_at = models.DateTimeField(
                 _('created at'),
                 auto_now_add=True,
                 db_index=True,
                 editable=False,
                 help_text = _('Non-editable, to be generated by system itself.'),
    )

    # Functions
    def __str__(self):
        return "Resource {0}".format(self.name)

    # Meta
    class Meta:
        verbose_name = _("Resource")
        verbose_name_plural = _("Resources")
        ordering = ["-created_at"]
        get_latest_by = "created_at"
        unique_together = ("name", "upstream_url", )

class ResourceLogs(models.Model):
    """
    Resource will also log its own life cycle using logging model.
    """
    # Relations
    resource = models.ForeignKey(Resource,
                 related_name = "resource_logs",
                 verbose_name = _("resource"),
                 help_text=_('Resource to which this log belongs too.'),
    )

    # Attributes
    logId = models.UUIDField(
            _('Log unique id'),
            unique=True,
            default=uuid.uuid4,
            editable=False,
            help_text = _('Non-editable, to be generated by system itself. To be returned in response, logs can be \
            fetched using this important in case do not want to share your primary key'),
    )
    started_at = models.DateTimeField(
                 _('Resource execution start time.'),
                 auto_now=False,
                 db_index=True,
                 help_text=_('When resource initiated its task.'),
    )
    ended_at = models.DateTimeField(
                 _('Resource execution end time.'),
                 auto_now=False,
                 db_index=True,
                 help_text=_('When resource completed its task.'),
    )
    dataIn = JSONField(
             _('Resource Request payload'),
             blank=True,
             null=True,
             help_text=_('Resource request payload, includes query_params, data etc.'),
    )
    dataOut = JSONField(
             _('Resource Request response'),
             blank=True,
             null=True,
             help_text=_('Response that is rerturned via Resource.'),
    )
    status = models.CharField(
             _('current state of resource request'),
             max_length=20,
             default='init',
             choices=RESOURCE_REQUEST_STATES,
             help_text=_('Resource Request state at any given time.'),
    )

    # Functions
    def __str__(self):
        return _(
                "Resource Log Id{0}".format(self.logId)
            )

    # Meta
    class Meta:
        verbose_name = _("Resource Logs")
        verbose_name_plural = _("Resources Logs")
        ordering = ["-id"]
        get_latest_by = "id"
