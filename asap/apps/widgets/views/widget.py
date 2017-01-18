#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route

from asap.apps.widgets.models.widget import Widget
from asap.apps.widgets.serializers.widget import WidgetSerializer
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin
from asap.router import Router


class WidgetViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer

    lookup_field = 'uuid'
    lookup_parent = [
        ('widget_locker_uuid', 'widgetlocker__uuid')
    ]

    def make_queryset(self):
        queryset = super(WidgetViewSet, self).make_queryset()
        if self.is_nested:
            return queryset

        # TODO
        # return all the widgets
        # available to the requesting user for direct access
        return queryset

    @detail_route(methods=['POST'])
    def execute(self, request, pk=None):
        # TODO execute/resume process
        return response.Response(status=status.HTTP_200_OK)


router = Router()
router.register('widgets', WidgetViewSet)
