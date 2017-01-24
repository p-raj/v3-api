#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import viewsets

from asap.apps.process.models import Process
from asap.apps.process.serializers import ProcessSerializer
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin


class ProcessViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer

    lookup_field = 'token'
    lookup_parent = [
        ('process_locker_uuid', 'processlocker__uuid')
    ]

    def make_queryset(self):
        queryset = super(ProcessViewSet, self).make_queryset()
        if self.is_nested:
            return queryset

        # TODO
        # return all the runtimes
        # available to the requesting user
        return queryset
