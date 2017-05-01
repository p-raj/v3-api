#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.decorators import detail_route

from asap.apps.process.models import ProcessLocker
from asap.apps.process.serializers import ProcessSerializer
from asap.apps.process.serializers.process_locker import ProcessLockerSerializer
from asap.core.filters.author_filter import AuthorFilter
from asap.core.views import AuthorableModelViewSet


class ProcessLockerViewSet(AuthorableModelViewSet, viewsets.ModelViewSet):
    queryset = ProcessLocker.objects.all()
    serializer_class = ProcessLockerSerializer
    filter_backends = (AuthorFilter,)

    lookup_field = 'uuid'

    @detail_route(methods=['POST'], lookup_field='uuid')
    def add(self, request, **kwargs):
        # expect either an existing instance
        # object/url or a new instance
        # FIXME
        # not perfect yet, but works :/
        process_serializer = ProcessSerializer(data=request.data, context=self.get_serializer_context())
        process_serializer.is_valid(raise_exception=True)
        process = process_serializer.save(author=request.user)

        process_locker = self.get_object()
        process_locker.processes.add(process)
        return self.retrieve(request, None, **kwargs)
