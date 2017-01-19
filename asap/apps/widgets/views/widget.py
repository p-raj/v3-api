#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- widgets.views.widget
~~~~~~~~~~~~~~

- This file contains the Widget service views, Every incoming http request to resolve any widget will come here.

 """

# future
from __future__ import unicode_literals

# DRF
from rest_framework import response, status, viewsets
from rest_framework.decorators import detail_route

# local
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin
from asap.router import Router

# own app
from asap.apps.widgets.models.widget import Widget
from asap.apps.widgets.serializers.widget import WidgetSerializer


class WidgetViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    """Widget Viewset , responsible for resolving and fetching a widget or fetch multiple widgets.

    """
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer

    lookup_field = 'uuid'
    lookup_parent = [
        ('widget_locker_uuid', 'widgetlocker__uuid')
    ]

    def make_queryset(self):
        """

        :return: queryset
        """
        queryset = super(WidgetViewSet, self).make_queryset()
        if self.is_nested:
            return queryset

        # TODO
        # return all the widgets
        # available to the requesting user for direct access
        return queryset

    @detail_route(methods=['POST'])
    def execute(self, request, pk=None):
        """

        :param request: Django request object.
        :param pk: Widget primary key
        :return:
        """
        # TODO execute/resume process
        return response.Response(status=status.HTTP_200_OK)


# Widget Routers
router = Router()
router.register('widgets', WidgetViewSet)
