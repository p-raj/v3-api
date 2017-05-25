#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

import yaml
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from mistralclient.api.base import APIException
from mistralclient.api.v2.workflows import WorkflowManager

from asap.apps.runtime.models.runtime import Runtime
from asap.libs.mistral.http_client import MistralHTTPClient

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Runtime)
def create_runtime_workflow(sender, **kwargs):
    instance = kwargs.get('instance')

    # we'll generate the initial workflow,
    # and prevent overriding it again
    instance.workflow = instance.workflow or instance.workflow_json

    workflow_manager = WorkflowManager(http_client=MistralHTTPClient())
    try:
        workflow = workflow_manager.get(instance.workflow_name)
        workflow_manager.update(yaml.dump(instance.workflow))
    except APIException as e:
        logger.warning(e)
        workflow = workflow_manager.create(yaml.dump(instance.workflow))[0]

    # prevent from getting into loop :)
    Runtime.objects.filter(pk=instance.pk).update(
        workflow_uuid=workflow.id,
        workflow=instance.workflow
    )


@receiver(post_delete, sender=Runtime)
def delete_workflow(sender, **kwargs):
    instance = kwargs.get('instance')
    workflow_manager = WorkflowManager(http_client=MistralHTTPClient())
    try:
        workflow_manager.delete(instance.workflow_uuid)
    except APIException as e:
        logger.warning(e)
