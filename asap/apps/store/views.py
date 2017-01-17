#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- store.views
~~~~~~~~~~~~~~

- This file contains store views means all http request/routers points to this file.
"""

# future
from __future__ import unicode_literals

# rest-framework
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions

# own app
from  asap.apps.store import models, resource

class ResourceViewSet(viewsets.GenericViewSet):
    """Resource Viewset, every resource http request handles by this class

    TODO : remove AllowAny permission with proper permission class

    """
    model = models.Resource
    permission_classes = (permissions.AllowAny, )

    def get_resource_object(self, token):
        """

        :param token: resource token
        :return: resource object
        """
        return self.model.objects.get(token=token)

    def resource_resolve(self, request, token, operation_id):
        """Resource POST request handles by this method

        :param request : Django request object.
        :param token: resource token, helps in identifying the resource
        :param operation_id : represents a specific operation of respective resource
        :return:
        """
        resourse_db_obj = self.get_resource_object(token)
        resource_cls = resource.Resource()
        operation_response = resource_cls.execute_operation(resourse_db_obj.upstream_url,
                                                         resourse_db_obj.schema,
                                                         operation_id,
                                                         data=request.data.dict()
                                                        )
        return Response(operation_response, status=status.HTTP_200_OK)
