#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import response, renderers, viewsets
from rest_framework.decorators import detail_route

from rest_framework_swagger.renderers import OpenAPIRenderer

from asap.apps.process.models import Process
from asap.apps.process.serializers import ProcessSerializer
from asap.core.filters.author_filter import AuthorFilter
from asap.core.permissions.is_author_or_read_only import IsAuthorOrReadOnly
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin


class ProcessViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (AuthorFilter,)

    lookup_field = 'uuid'
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

    @detail_route(renderer_classes=[renderers.JSONRenderer])
    def schema(self, request, **kwargs):
        instance = self.get_object()
        return response.Response(instance.schema)

    @detail_route(renderer_classes=[renderers.CoreJSONRenderer])
    def client(self, request, **kwargs):
        instance = self.get_object()
        return response.Response(instance.schema_client)

    @detail_route(renderer_classes=[OpenAPIRenderer])
    def server(self, request, **kwargs):
        instance = self.get_object()
        return response.Response(instance.schema_server)

    @detail_route(renderer_classes=[renderers.CoreJSONRenderer])
    def execute(self, request, **kwargs):
        client = self.get_object().client
        return response.Response(client.execute(request), content_type='application/json')
