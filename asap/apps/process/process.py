#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- process.process
~~~~~~~~~~~~~~

-   This file contains classes/functions related to Process

 """

# future
from __future__ import unicode_literals

# DRF
from rest_framework.exceptions import ValidationError

# 3rd party
import requests

# own app
from asap.apps.process import models, RESOURCE_UPSTREAM_URL


class Process(object):
    """A Process class for accessing various process operations and RESTful service.

    """
    model = models.Process
    logging_cls = None

    def __init__(self, code, logging_cls):
        """

        :param code: process code
        :param logging_cls: Logging class instance.
        """
        self.logging_cls = logging_cls
        self.process_obj = self.model.objects.get(code=code)

    def execute_process(self, data={}):
        """

        :param data: payload to sent with request
        :return: depends on resource being called by Process
        """
        resource_token = self.process_obj.resource_token
        url = str(RESOURCE_UPSTREAM_URL).format(
            resource_token=resource_token,
            operation=self.process_obj.operation,
        )

        self.logging_cls.handshake(resource_token, data)  # execution handover initiated

        rq = requests.post(url=url,
                           data=data
        )
        if rq.status_code == requests.codes.ok:
            self.logging_cls.handshake_succeed(resource_token, data, rq)  # execution handover status
            return rq.json()

        self.logging_cls.handshake_failed(resource_token, data, rq.status_code, rq.json())  # execution handover status
        raise ValidationError(rq.json())
