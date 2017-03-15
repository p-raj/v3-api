#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import viewsets

from asap.apps.organizations.serializers.services import Service, ServiceSerializer
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin


class ServiceViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    lookup_parent = [
        ('organization_pk', 'organization')
    ]
