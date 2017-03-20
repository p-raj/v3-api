#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- widgets.signals.widget
~~~~~~~~~~~~~~

- This file contains the Widget signals.

 """

# future
from __future__ import unicode_literals
import copy
import requests

from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.urls import reverse_lazy

from asap.apps.widgets.models.widget import Widget

ProcessLocker_URL = 'http://localhost:8000/api/v1/process-lockers/{pl_uuid}/processes/'

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


@receiver(post_save, sender=Widget)
def create_widget_schema(sender, **kwargs):
    """this signal is used to generate schema for sender-widget of this signal.

    :param sender: sender or initiator og this signal
    :param kwargs: keyword arguments
    :return:
    """
    if not kwargs.get('created'):
        return

    # fetch the process using the process locker token
    # and build the widget schema according OpenAPI Spec
    instance = kwargs.get('instance')
    response = requests.get(ProcessLocker_URL.format(pl_uuid=instance.process_locker_uuid))

    # move these lame tasks to some place else
    # and make these smart
    processes = response.json().get('results')

    # copy all the definitions that the process carries
    # currently we'll limit the process locker service from
    # creating a locker that has processes from different resources
    # for p in processes:
    #     schema['definitions'].update(**p.get('endpoint_schema').get('definitions', {}))
    #     schema['securityDefinitions'].update(**p.get('endpoint_schema').get('securityDefinitions', {}))

    # this is the initial schema and will be presented
    # to the admin for adding static data and modification
    instance.processes_json = processes
    instance.save()
