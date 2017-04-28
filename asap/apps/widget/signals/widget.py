#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- widgets.signals.widget
~~~~~~~~~~~~~~

- This file contains the Widget signals.

 """
import logging
import requests
import yaml

from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from asap.apps.widget.models.widget import Widget
from asap.apps.widget.views.process_service import MISTRAL_SERVER
from mistralclient.api.base import APIException
from mistralclient.api.v2.client import httpclient
from mistralclient.api.v2.workflows import WorkflowManager

logger = logging.getLogger(__name__)

ProcessLocker_URL = 'http://localhost:8001/api/v1/process-lockers/{pl_uuid}/processes/'

swagger_dict = {
    'swagger': '2.0',
    'info': {
        'title': '',
        'version': '1.0.0'
    },
    'paths': {},
    'definitions': {},
    'securityDefinitions': {}
}


# @receiver(post_save, sender=Widget)
def create_widget_schema(sender, **kwargs):
    """this signal is used to generate schema for sender-widget of this signal.

    :param sender: sender or initiator og this signal
    :param kwargs: keyword arguments
    :return:
    """
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

    workflow_manager = WorkflowManager(http_client=httpclient.HTTPClient(MISTRAL_SERVER))
    try:
        workflow = workflow_manager.get(instance.workflow_name)
        workflow_manager.update(yaml.dump(instance.workflow_json))
    except APIException as e:
        logger.warning(e)
        workflow = workflow_manager.create(yaml.dump(instance.workflow_json))[0]

    # prevent from getting into loop :)
    Widget.objects.filter(pk=instance.pk).update(
        processes_json=instance.processes_json,
        workflow_uuid=workflow.id
    )

    # instance.processes_json = processes
    # instance.workflow_uuid = workflow.id
    # instance.save()
