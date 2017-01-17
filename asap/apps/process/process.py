#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- process.process
~~~~~~~~~~~~~~

-   This file contains classes/functions related to Process

 """

# future
from __future__ import unicode_literals

# 3rd party
import requests

# own app
from asap.apps.process import models, RESOURCE_UPSTREAM_URL

class Process(object):
    """A Process class for accessing various process operations and RESTful service.

    """
    model = models.Process
    def __init__(self, code):
        """

        :param code: process code
        """
        self.process_obj = self.model.objects.get(code=code)

    def execute_process(self, data={}):
        """

        :param data: payload to sent with request
        :return: depends on resource being called by Process
        """
        url = str(RESOURCE_UPSTREAM_URL).format(
            resource_token=self.process_obj.resource_token,
            operation=self.process_obj.operation,
        )
        rq = requests.post(url=url,
                           data=data
        )
        return  rq.json()