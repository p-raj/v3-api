#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from rest_framework import viewsets, response
from rest_framework.decorators import list_route
from rest_framework.permissions import AllowAny

from asap.apps.widget.models.widget import Widget
from asap.apps.widget.serializers.widget import WidgetSerializer
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin

logger = logging.getLogger(__name__)


class WidgetViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    permission_classes = (AllowAny,)

    lookup_field = 'uuid'
    lookup_parent = [
        ('widget_locker_uuid', 'widgetlocker__uuid')
    ]
    lookup_fields = (
        'name', 'description'
    )
    ordering_fields = (
        'created_at', 'modified_at'
    )

    def get_queryset(self):
        queryset = super(WidgetViewSet, self).get_queryset()
        if self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset

    @list_route(permission_classes=(AllowAny,))
    def system(self, request, *args, **kwargs):
        instance = self.queryset.filter(name='__system__').first()
        serializer = self.get_serializer_class()(
            instance=instance,
            context={
                'request': request
            }
        )
        return response.Response(serializer.data)
