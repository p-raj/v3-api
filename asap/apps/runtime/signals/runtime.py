#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

import yaml
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from asap.apps.runtime.models.runtime import Runtime
from asap.apps.widget.views.process_service import MISTRAL_SERVER
from mistralclient.api.base import APIException
from mistralclient.api.v2.client import httpclient
from mistralclient.api.v2.workflows import WorkflowManager

logger = logging.getLogger(__name__)


# @receiver(post_save, sender=Runtime)
def create_runtime_workflow(sender, **kwargs):
    instance = kwargs.get('instance')
    workflow_manager = WorkflowManager(http_client=httpclient.HTTPClient(MISTRAL_SERVER))
    try:
        workflow = workflow_manager.get(instance.workflow_name)
        workflow_manager.update(yaml.dump(instance.workflow_json))
    except APIException as e:
        logger.warning(e)
        workflow = workflow_manager.create(yaml.dump(instance.workflow_json))[0]

    # prevent from getting into loop :)
    Runtime.objects.filter(pk=instance.pk).update(
        workflow_uuid=workflow.id
    )
