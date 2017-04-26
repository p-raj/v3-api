#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import kinto_http
from kinto_http.exceptions import KintoException
from rest_framework import response, status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.reverse import reverse_lazy

from asap.apps.vrt.models.session import Session
from asap.apps.vrt.serializers.session import SessionSerializer
from asap.core.permissions.is_author_or_read_only import IsAuthorOrReadOnly
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin

# FIXME
KINTO_BUCKET = 'runtimes'
KINTO_COLLECTION = 'sessions'


class SessionViewSet(AuthorableModelViewSet, DRFNestedViewMixin,
                     viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = (AllowAny,)

    lookup_field = 'uuid'
    lookup_parent = [
        ('runtime_uuid', 'runtime__uuid')
    ]

    # abstract out storage :)
    # FIXME
    kinto = kinto_http.Client('http://localhost:8888', auth=('test', 'test'))

    def create(self, request, *args, **kwargs):
        data = request.data.get('data', {})
        session = self.kinto.create_record(
            data if type(data) == dict else json.loads(data),
            bucket=KINTO_BUCKET,
            collection=KINTO_COLLECTION
        )

        # we are storing all the sessions using kinto
        # this is just to prevent lot of changes on the client
        request.data.update(uuid=session.get('data').get('id'))

        self.filter_nested_queryset(**kwargs)
        if self.is_nested:
            # we don't need to ask for the runtime to which the
            # session will be associated when the url is nested
            request.data.update(runtime=reverse_lazy('runtime-detail', kwargs={
                'uuid': kwargs.get('runtime_uuid')
            }))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # FIXME
        serializer.instance.uuid = session.get('data').get('id')
        serializer.instance.save()

        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        data = request.data.get('data', {})
        data = data if type(data) == dict else json.loads(data)
        self.kinto.update_record(
            data,
            id=self.get_object().uuid,
            bucket=KINTO_BUCKET,
            collection=KINTO_COLLECTION
        )
        return super(SessionViewSet, self).update(request, *args, **kwargs)

    def get_object(self):
        instance = super(SessionViewSet, self).get_object()
        try:
            session = self.kinto.get_record(
                id=instance.uuid,
                bucket=KINTO_BUCKET,
                collection=KINTO_COLLECTION
            )
            instance.data.update(**session.get('data'))
        except KintoException:
            # FIXME
            pass
        return instance

    @detail_route(permission_classes=[AllowAny], methods=['post'])
    def set(self, request, **kwargs):
        data = request.data
        data = data if type(data) == dict else json.loads(data)
        data = {
            request.META.get('HTTP_PROCESS', 'invalid'): data
        }
        r = self.kinto.update_record(
            data,
            id=self.get_object().uuid,
            bucket=KINTO_BUCKET,
            collection=KINTO_COLLECTION
        )
        return response.Response(r)

    @detail_route(permission_classes=[AllowAny], methods=['get', 'post'])
    def get(self, request, **kwargs):
        instance = self.get_object()
        return response.Response(instance.data.get(request.META.get('HTTP_PROCESS', 'invalid'), {}))
