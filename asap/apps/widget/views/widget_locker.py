#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import viewsets
from rest_framework.decorators import detail_route

from asap.apps.widget.models.widget_locker import WidgetLocker
from asap.apps.widget.serializers.widget import WidgetSerializer
from asap.apps.widget.serializers.widget_locker import WidgetLockerSerializer
from asap.core.views import AuthorableModelViewSet


class WidgetLockerViewSet(AuthorableModelViewSet, viewsets.ModelViewSet):
    queryset = WidgetLocker.objects.all()
    serializer_class = WidgetLockerSerializer

    lookup_field = 'uuid'

    @detail_route(methods=['POST'], lookup_field='uuid')
    def add(self, request, **kwargs):
        # expect either an existing instance
        # object/url or a new instance
        # FIXME
        # not perfect yet, but works :/
        widget_serializer = WidgetSerializer(data=request.data, context=self.get_serializer_context())
        widget_serializer.is_valid(raise_exception=True)
        widget = widget_serializer.save(author=request.user)

        widget_locker = self.get_object()
        widget_locker.widgets.add(widget)
        return self.retrieve(request, None, **kwargs)
