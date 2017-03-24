#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.service_vault.views
~~~~~~~~~~~~~~~~~~~~~~~~~~

- This file contains service-vault views means all http request/routers points to this file.
"""

# future
from __future__ import unicode_literals

# 3rd party

# rest-framework
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status

# local

# own app
from asap.apps.service_vault import models, serializers


class ServiceVaultViewSet(viewsets.ModelViewSet):
    """Service Vault Viewset, every resource http request handles by this class

    **Query Parameters**:
        `is_public` -- true/false_, get public or private services only.

    """
    model = models.ServiceVault
    queryset = model.objects.all()
    # TODO : remove AllowAny permission with proper permission class
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializers.ServiceVaultSerializer

    def get_queryset(self, *args, **kwargs):
        """
        Optionally restricts the returned services to public or private.
        by filtering against a `is_public` query parameter in the URL.
        """
        queryset = super(ServiceVaultViewSet, self).get_queryset(*args, **kwargs)
        if 'is_public' in self.request.query_params:
            if self.request.query_params.get('is_public') == 'true':
                queryset = queryset.filter(is_public=True)
            elif self.request.query_params.get('is_public') == 'false':
                queryset = queryset.filter(is_public=False)
        return queryset

    def apis(self, request, pk=None):
        """

        :param request: Django request param
        :param pk: service vault primary key
        :return: Service APIS or operations in swagger
        """
        response = self.get_object().get_operations()
        return Response({'operations': response}, status=status.HTTP_200_OK)