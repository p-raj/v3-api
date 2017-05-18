#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

import requests
import yaml
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from mistralclient.api.base import APIException
from mistralclient.api.v2.workflows import WorkflowManager

from asap.apps.widget.models.widget import Widget
from asap.libs.mistral.http_client import MistralHTTPClient

logger = logging.getLogger(__name__)

ProcessLocker_URL = 'http://172.20.0.1:8000/api/v1/process-lockers/{pl_uuid}/processes/'


@receiver(post_save, sender=Widget)
def create_widget_schema(sender, **kwargs):
    instance = kwargs.get('instance')

    # fetch the process using the process locker token
    # and build the widget schema according OpenAPI Spec
    response = requests.get(ProcessLocker_URL.format(pl_uuid=instance.process_locker_uuid))

    # move these lame tasks to some place else
    # and make these smart
    instance.processes_json = response.json().get('results')

    # copy all the definitions that the process carries
    # currently we'll limit the process locker service from
    # creating a locker that has processes from different resources
    # for p in processes:
    #     schema['definitions'].update(**p.get('endpoint_schema').get('definitions', {}))
    #     schema['securityDefinitions'].update(**p.get('endpoint_schema').get('securityDefinitions', {}))

    # this is the initial schema and will be presented
    # to the admin for adding static data and modification

    # we'll generate the initial workflow,
    # and prevent overriding it again
    instance.workflow = instance.workflow or instance.workflow_json

    workflow_manager = WorkflowManager(http_client=MistralHTTPClient())
    try:
        workflow = workflow_manager.get(instance.workflow_name)
        workflow_manager.update(yaml.dump(instance.workflow))
    except APIException as e:
        logger.warning(e)
        workflow = workflow_manager.create(yaml.dump(instance.workflow_json))[0]

    # prevent from getting into loop :)
    Widget.objects.filter(pk=instance.pk).update(
        processes_json=instance.processes_json,
        workflow_uuid=workflow.id,
        workflow=instance.workflow
    )


@receiver(post_delete, sender=Widget)
def delete_workflow(sender, **kwargs):
    instance = kwargs.get('instance')
    workflow_manager = WorkflowManager(http_client=MistralHTTPClient())
    try:
        workflow_manager.delete(instance.workflow_uuid)
    except APIException as e:
        logger.warning(e)
