#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- micro_services.state_machine.models
~~~~~~~~~~~~~~

- This file contains models of state machine micro service
"""

# future
from __future__ import unicode_literals

# 3rd party

# Django
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# local

# own app
from asap.micro_services.state_machine import config


class TransactionStateMachine(models.Model):
    """Manage Current State of any Task.

    """
    # Attributes
    task_name = models.CharField(
        _('task name'),
        max_length=30,
        help_text=_('Required. 30 characters or fewer.'),
    )
    task_identifier = models.CharField(
        _('any unique identifier of any task'),
        max_length=200,
        help_text=_('Required. 200 characters or fewer.'),
    )
    state = models.CharField(
        _('current state of any task'),
        max_length=20,
        default=config.INIT,
        choices=config.STATES,
        help_text=_('Task state at any given time.'),
    )
    created_at = models.DateTimeField(
        _('Task state activity create time.'),
        auto_now=True,
        db_index=True,
    )
    modified_at = models.DateTimeField(
        _('Task state activity modify time.'),
        auto_now=True,
        db_index=True,
    )

    # Meta
    class Meta:
        verbose_name = _("Transaction State Machine")
        verbose_name_plural = _("Transaction State Machine")
        ordering = ["-id"]
        get_latest_by = "id"

    # Functions
    def __str__(self):
        return "Transaction id {transaction_id} -- task-identifier {task_identifier} -- state {state}".format(
            transaction_id=self.id,
            task_identifier=self.task_identifier,
            state=self.state
        )


class TransactionLifeCycle(models.Model):
    """Manage Any Transaction life cycle.

        - We will use Django GenericForeignKey (EAV) to store service which was called by task.
         Why ? - Right now we only support HTTP services but later we will support many others, so it is to be well
         prepare for that.

    """
    task = models.ForeignKey(TransactionStateMachine,
                             verbose_name=_('transaction state machine'))
    content_type = models.ForeignKey(ContentType,
                                     db_index=True,
                                     help_text=_('Content Type of Object you want tyo map.'))
    object_id = models.PositiveIntegerField(
        _('id of object you want to map'),
        db_index=True)
    entity = GenericForeignKey('content_type', 'object_id')
    state = models.CharField(
        _('current state of any task'),
        max_length=20,
        default=config.INIT,
        choices=config.STATES,
        help_text=_('Task state at any given time.'),
    )
    created_at = models.DateTimeField(
        _('Task state activity create time.'),
        auto_now=True,
        db_index=True,
    )

    # Meta
    class Meta:
        verbose_name = _("Transaction Life Cycle")
        verbose_name_plural = _("Transaction Life Cycle")
        ordering = ["-id"]
        get_latest_by = "id"

    # Functions
    def __str__(self):
        return "life cycle id {cycle_id} -- state {state}".format(
            cycle_id=self.id,
            state=self.state
        )


class HttpService(models.Model):
    """Http service Model

    """
    upstream_url = models.URLField(
        _('upstream url of HTTP service.'),
        max_length=200,
        help_text=_('Required. 200 characters or fewer.'),
    )
    method = models.CharField(
        _('Service Supported Method '),
        max_length=6,
        default=config.POST,
        choices=config.METHODS,
        help_text=_('Service Supported Methods.'),
    )
    headers = JSONField(
        _('Request Headers'),
        blank=True,
        null=True,
        help_text=_('Request Headers.'),
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
    created_at = models.DateTimeField(
        _('service request time.'),
        auto_now=True,
        db_index=True,
    )

    # Meta
    class Meta:
        verbose_name = _("HTTP Service")
        verbose_name_plural = _("HTTP Service")
        ordering = ["-id"]
        get_latest_by = "id"

        # Functions
    def __str__(self):
        return "service id {service_id}".format(
            service_id=self.id,
        )
