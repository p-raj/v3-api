#!/usr/bin/python
# -*- coding: utf-8 -*-
from rest_framework import renderers, response, viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework_swagger.renderers import OpenAPIRenderer

from asap.apps.process.models import Process
from asap.apps.process.serializers import ProcessSerializer
from asap.utils.views import AuthorableModelViewSet, DRFNestedViewMixin


class ProcessViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    permission_classes = (AllowAny,)

    lookup_field = 'uuid'
    lookup_parent = [
        ('widget_uuid', 'widget_widget_widget__uuid')
    ]
    lookup_fields = (
        'name', 'description'
    )
    ordering_fields = (
        'created_at', 'modified_at'
    )

    def get_queryset(self):
        queryset = super(ProcessViewSet, self).get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
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
