#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- micro_services.authorization.views
~~~~~~~~~~~~~~

- This file contains authorization service actions like creating new permissions , validating access.
"""

# future
from __future__ import unicode_literals

# 3rd party

# rest-framework
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

# Django
from django.shortcuts import get_object_or_404


# local

# own app
from asap.micro_services.authorization import serializers, models


class AuthorizationViewSet(viewsets.GenericViewSet):
    """Authorization Viewset, every authorization http request handles by this class

    """
    model = models.Authorization
    serializer_class = serializers.AuthorizationSerializer
    # TODO : remove AllowAny permission with proper permission class
    permission_classes = (permissions.AllowAny, )

    def get_object(self, source, target):
        """

        :return: Authorization object
        """
        return get_object_or_404(models.Authorization, source=source,
                                                target=target)

    def create_perm(self, request):
        """

        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update_perm(self, request):
        """

        """
        obj = self.get_object(request.data.get('source'), request.data.get('target'))
        serializer = self.get_serializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def has_perm(self, request):
        """check authorization w.r.t target

        GET Data example :

        {
            "access_type": "read",
            "target": "P1",
            "source": "W1"
        }

        """
        serializer = serializers.CheckAccessSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        obj = self.get_object(serializer.data.get('source'), serializer.data.get('target'))

        response = serializer.check_perm(obj, serializer.data.get('access_type'))

        return Response(response, status=status.HTTP_200_OK)




