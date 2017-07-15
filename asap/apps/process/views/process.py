#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from rest_framework import renderers, response, viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework_swagger.renderers import OpenAPIRenderer

from asap.apps.process.models import Process
from asap.apps.process.serializers import ProcessSerializer
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin


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

    @detail_route(
        methods=['GET', 'POST'],
        renderer_classes=[renderers.CoreJSONRenderer],
        permission_classes=(AllowAny,)
    )
    def execute(self, request, **kwargs):
        # TODO: move the execute detail route to a separate API View
        # since it prevents us from applying the author filter,
        # which makes sense for the other routes
        try:
            client = self.get_object().client

            # default content-type is coreapi+json
            data = client.execute(params=request.data, **kwargs)

            # FIXME
            meta = getattr(data, 'title', '200 OK') or '200 OK'
            meta = meta if type(meta) == str else '200 OK'
            return response.Response(
                data,
                status=int(meta.split()[0]),
                content_type=request.content_type
            )
        except ValidationError as e:
            return response.Response({
                'errors': e.message.args
            },
                status=HTTP_400_BAD_REQUEST,
                content_type='application/json'
            )
