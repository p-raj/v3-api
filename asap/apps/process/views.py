#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- process.views
~~~~~~~~~~~~~~

- This file contains process views means all http request/routers points to this file.
"""

# future
from __future__ import unicode_literals

# rest-framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions

# own app
from  asap.apps.process import models, process

class ProcessLockerViewSet(viewsets.GenericViewSet):
    """Process Locker Viewset, every process http request handles by this class

    TODO : remove AllowAny permission with proper permission class

    """
    model = models.ProcessLocker
    permission_classes = (permissions.AllowAny, )

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
            process_cls = process.Process(process_token)
            process_response.append(process_cls.execute_process(data))
        return process_response

    def process_locker_resolve(self, request, token):
        """Process POST request handles by this method

        :param request : Django request object.
        :param token: process locker token, helps in identifying the locker
        :return: depends on process response/execution
        """
        process_locker_obj = self.get_locker_object(token)

        response = self._read_process_locker_rules(process_locker_obj)

        return Response(response, status=status.HTTP_200_OK)
