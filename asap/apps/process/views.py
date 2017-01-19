#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- process.views
~~~~~~~~~~~~~~

- This file contains process views means all http request/routers points to this file.
"""

# future
from __future__ import unicode_literals

# 3rd party
import uuid

# rest-framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions

# local
from asap.apps.logs import logging

# own app
from asap.apps.process import models, process


class ProcessLockerViewSet(viewsets.GenericViewSet):
    """Process Locker Viewset, every process http request handles by this class

    TODO : remove AllowAny permission with proper permission class

    """
    model = models.ProcessLocker
    permission_classes = (permissions.AllowAny, )
    actor = 'process'
    session = uuid.uuid4()
    logging_cls = None
    token = None

    def get_locker_object(self, token):
        """

        :param token: process locker token
        :return: Process locker object
        """
        return self.model.objects.get(token=token)

    def _read_process_locker_rules(self, obj):
        """Read rules defined for locker

        :param obj: process locker object.
        :return: all process combined response
        """
        data = {'organization_id': '1', 'id': '1'}

        process_response = []
        for process_token in obj.rules:
            process_cls = process.Process(process_token, self.logging_cls)
            process_response.append(process_cls.execute_process(data))
        return process_response

    def _create_log_instance(self, request, token):
        """

        :param request : Django request object.
        :return:
        """
        self.logging_cls = logging.ServiceLogging(
                                    self.actor,
                                    token,
                                    self.session,
                                    payload=request.data or dict())

    def process_locker_resolve(self, request, token):
        """Process POST request handles by this method

        :param request : Django request object.
        :param token: process locker token, helps in identifying the locker
        :return: depends on process response/execution
        """
        # Start logging of Process
        self._create_log_instance(request, token)
        self.logging_cls.initialize()  # initialize process logging

        process_locker_obj = self.get_locker_object(token)

        response = self._read_process_locker_rules(process_locker_obj)

        return Response(response, status=status.HTTP_200_OK)

    def finalize_response(self, request, response, *args, **kwargs):
        """Log Process before sending final response

        :param request: django request object
        :param response: response to be sent to client
        :param args: function arguments
        :param kwargs: function keyword arguments
        :return: returns final response

        Note :
            if response code is 2xx then we call success log method else false method will be called
        """
        if self.logging_cls is None:
            self._create_log_instance(request, kwargs.get('token'))

        if str(response.status_code).startswith('2'):
            self.logging_cls.success(response)  # logged as success
        else:
            self.logging_cls.fail(response)  # logged as failure
        return super(ProcessLockerViewSet, self).finalize_response(request, response, *args, **kwargs)