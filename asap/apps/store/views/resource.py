#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- store.views.resource
~~~~~~~~~~~~~~

- This file contains resource views means all http request/routers points to this file.
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
from asap.apps.store import models
from asap.apps.store.core import resource

class ResourceViewSet(viewsets.GenericViewSet):
    """Resource Viewset, every resource http request handles by this class

    TODO : remove AllowAny permission with proper permission class

    """
    model = models.Resource
    permission_classes = (permissions.AllowAny, )
    actor = 'resource'
    session = uuid.uuid4()
    logging_cls = None

    def get_resource_object(self, token):
        """

        :param token: resource token
        :return: resource object
        """
        return self.model.objects.get(token=token)

    def _create_log_instance(self, request, token):
        """

        :param request : Django request object.
        :param token : process token.
        :return: logging class instance
        """
        self.logging_cls = logging.ServiceLogging(
            self.actor,
            token,
            self.session,
            payload=request.data or dict())

    def resource_resolve(self, request, token, operation_id):
        """Resource POST request handles by this method

        :param request : Django request object.
        :param token: resource token, helps in identifying the resource
        :param operation_id : represents a specific operation of respective resource
        :return:
        """

        # Start logging of Process
        self._create_log_instance(request, token)
        self.logging_cls.initialize()  # initialize process logging

        resourse_db_obj = self.get_resource_object(token)

        resource_cls = resource.Resource(self.logging_cls)
        operation_response = resource_cls.execute_operation(resourse_db_obj.upstream_url,
                                                            resourse_db_obj.schema,
                                                            operation_id,
                                                            data=request.data,
                                                            )
        return Response(operation_response, status=status.HTTP_200_OK)

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
        return super(ResourceViewSet, self).finalize_response(request, response, *args, **kwargs)