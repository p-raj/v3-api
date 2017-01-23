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
from rest_framework import viewsets, permissions

# own app
from asap.apps.widgets.models.widget import Widget
from asap.apps.widgets.serializers.widget import WidgetSerializer
from asap.core.views import AuthorableModelViewSet, DRFNestedViewMixin


class WidgetViewSet(AuthorableModelViewSet, DRFNestedViewMixin, viewsets.ModelViewSet):
    """Widget Viewset , responsible for resolving and fetching a widget or fetch multiple widgets.

    """
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    permission_classes = (permissions.AllowAny,)

    lookup_field = 'token'

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
