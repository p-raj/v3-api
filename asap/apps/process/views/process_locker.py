#!/usr/bin/python
# -*- coding: utf-8 -*-

from asap.apps.process.models import ProcessLocker
from asap.apps.process.serializers.process_locker import ProcessLockerSerializer
from asap.core.views import AuthorableModelViewSet

from rest_framework import viewsets, permissions


class ProcessLockerViewSet(AuthorableModelViewSet, viewsets.ModelViewSet):
    queryset = ProcessLocker.objects.all()
    serializer_class = ProcessLockerSerializer
    # TODO : remove AllowAny permission with proper permission class
    permission_classes = (permissions.AllowAny,)

    lookup_field = 'token'
