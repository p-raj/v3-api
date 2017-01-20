#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- logging.logging
~~~~~~~~~~~~~~


- This file contains a class which can be used to log various stages of a service
 """

# future
from __future__ import unicode_literals

# core
from django.utils import timezone

# own app
from asap.apps.logs.models import ServiceLogs


class ServiceLogging(object):
    """
    Ref : Different logging states and Actor Types

    LOGGING_STATES = (
        ('init', 'Initialize'),
        ('in-progress', 'In Progress'),
        ('wait', 'Waiting'),
        ('handshake', 'Handshake'),
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
    """
    model = ServiceLogs

    def __init__(self, actor, actor_token, session, payload):
        """
        :param actor: actor type for whom you want to log.
        :param actor_token: actor token for whom you want to log.
        :param session: session of any log life cycle.
        :param payload: payload sent in http request.
        """
        self.fields = dict()
        self.actor = actor
        self.actor_token = actor_token
        self.session = session
        self.fields.update({
            'actor': actor,
            'dataIn': payload,
            'session': session,
            'actor_token': actor_token})

    def _log_db_entry(self, data):
        """

        :return: Logging object
        """
        self.fields.update({'started_at': timezone.now()})

        data.update(**self.fields)
        return self.model.objects.create(**data)

    def initialize(self):
        """implies initialization of any process, to be logged with state=init

        :return: logging object
        """
        data = {'state': 'init'}  # set life cycle state = init
        return self._log_db_entry(data)

    def start_execution(self):
        """implies service have started execution, to be logged with state=in-process

        :return: logging object
        """
        data = {'state': 'in-process'}  # set life cycle state = in-process
        return self._log_db_entry(data)

    def handshake(self, handshake_token, payload):
        """implies service have handover his execution to another service, to be logged with state=handshake

        :param handshake_token: token of service to whom execution is handover.
        :param payload: payload sent in http request.
        :return: logging object
        """
        data = {
                'state': 'handshake-initialize',
                'handshake_token': handshake_token,
                'dataIn': payload
        }  # set life cycle state = handshake
        return self._log_db_entry(data)

    def handshake_succeed(self, handshake_token, payload, response):
        """implies service handshake have succeeded , to be logged with state=handshake-succeed

        :param handshake_token: token of service to whom execution is handover.
        :param payload: payload sent in http request.
        :param response: handshake response.
        :return: logging object
        """
        data = {
                'state': 'handshake-succeed',
                'handshake_token': handshake_token,
                'handshake_status': True,
                'dataIn': payload,
                'status_code': response.status_code,
                'dataOut': response.json()
        }  # set life cycle state = fwd
        return self._log_db_entry(data)

    def handshake_failed(self, handshake_token, payload, status_code, response):
        """implies service handshake have failed, to be logged with state=handshake-failed

        :param handshake_token: token of service to whom execution is handover.
        :param payload: payload sent in http request.
        :param status_code: handshake status_code.
        :param response: handshake response.
        :return: logging object
        """
        data = {
                'state': 'handshake-failed',
                'handshake_token': handshake_token,
                'handshake_status': False,
                'dataIn': payload,
                'status_code': status_code,
                'dataOut': response
        }  # set life cycle state = fwd
        return self._log_db_entry(data)

    def wait(self, response):
        """implies service is waiting for some action or input, to be logged with state=wait

        :param response: DRF viewset Response object.
        :return: logging object
        """
        data = {
                'state': 'wait',
                'handshake_token': None,
                'handshake_status': False,
                'status_code': response.status_code,
                'dataOut': response.data
        }  # set life cycle state = wait
        return self._log_db_entry(data)

    def fail(self, response):
        """implies process have failed execution, to be logged with state=failed

        :param response: DRF viewset Response object.
        :return: logging object
        """
        data = {
                'state': 'failed',
                'handshake_token': None,
                'handshake_status': False,
                'status_code': response.status_code,
                'dataOut': response.data,
                'ended_at': timezone.now()
        }  # set life cycle state = failed
        return self._log_db_entry(data)

    def success(self, response):
        """implies process have successfully executed, to be logged with state=succeeded

        :param response: DRF viewset Response object.
        :return: logging object
        """
        data = {
                'state': 'succeeded',
                'handshake_token': None,
                'handshake_status': False,
                'status_code': response.status_code,
                'dataOut': response.data,
                'ended_at': timezone.now()
        }  # set life cycle state = succeeded
        return self._log_db_entry(data)

    def update_endtime(self, instance):
        """update end-time of any log object.

        :param instance: log object you want to update.
        :return: updated log object
        """
        instance.ended_at = timezone.now()
        return instance.save()
